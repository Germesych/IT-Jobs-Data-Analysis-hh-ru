"""
Асинхронный проверщик вакансий hh.ru с ограничением 1 соединение на 1 прокси
"""

import aiohttp
import asyncio
import random
import logging
from typing import List, Optional, Dict, Any, Union
import backoff
from dataclasses import dataclass
import time
from collections import deque
from src.database.db_manager import get_open_vacancies_links

# Детальная настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class ProxyConfig:
    """Конфигурация HTTP прокси-сервера"""

    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

    def __hash__(self):
        """Делаем ProxyConfig хешируемым для использования в set()"""
        return hash((self.host, self.port, self.username, self.password))

    def __eq__(self, other):
        """Для корректной работы в set() нужен также __eq__"""
        if not isinstance(other, ProxyConfig):
            return False
        return (
            self.host == other.host
            and self.port == other.port
            and self.username == other.username
            and self.password == other.password
        )

    def get_proxy_url(self) -> str:
        """Формирует URL для HTTP прокси"""
        if self.username and self.password:
            return f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"http://{self.host}:{self.port}"


class ProxyManager:
    """Менеджер прокси с ограничением 1 соединение на прокси"""

    def __init__(self, proxies: List[ProxyConfig]):
        self.proxies = proxies
        self.available_proxies = deque(proxies)  # Очередь свободных прокси
        self.locked_proxies = set()  # Занятые прокси
        self.lock = asyncio.Lock()

    async def get_proxy(self) -> Optional[ProxyConfig]:
        """Получает свободный прокси. Если нет свободных - ждет"""
        async with self.lock:
            if self.available_proxies:
                proxy = self.available_proxies.popleft()
                self.locked_proxies.add(proxy)
                logger.debug(f"🔄 Взяли прокси {proxy.host}:{proxy.port} в работу")
                return proxy
            else:
                logger.debug("⏳ Нет свободных прокси, ждем...")
                return None

    async def release_proxy(self, proxy: ProxyConfig):
        """Освобождает прокси для повторного использования"""
        async with self.lock:
            if proxy in self.locked_proxies:
                self.locked_proxies.remove(proxy)
                self.available_proxies.append(proxy)
                logger.debug(f"✅ Освободили прокси {proxy.host}:{proxy.port}")

    def get_available_count(self) -> int:
        """Возвращает количество доступных прокси"""
        return len(self.available_proxies)

    def get_locked_count(self) -> int:
        """Возвращает количество занятых прокси"""
        return len(self.locked_proxies)


def load_proxies_from_config(proxy_list: List[Dict]) -> List[ProxyConfig]:
    """Загружает список HTTP прокси"""
    proxies = []
    for proxy_data in proxy_list:
        proxy = ProxyConfig(
            host=proxy_data["host"],
            port=proxy_data["port"],
            username=proxy_data.get("username"),
            password=proxy_data.get("password"),
        )
        proxies.append(proxy)
    return proxies


async def test_proxy_connection(
    proxy_url: str, test_url: str = "https://httpbin.org/ip"
) -> bool:
    """Тестирует работоспособность прокси"""
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(test_url, proxy=proxy_url, ssl=False) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Прокси работает. IP: {data.get('origin')}")
                    return True
                else:
                    logger.error(f"❌ Прокси вернул статус {response.status}")
                    return False
    except Exception as e:
        logger.error(f"❌ Прокси не работает: {str(e)}")
        return False


async def test_all_proxies(proxies: List[ProxyConfig]) -> List[ProxyConfig]:
    """Тестирует все прокси и возвращает только рабочие"""
    logger.info("🧪 Тестируем прокси...")

    working_proxies = []
    test_url = "https://httpbin.org/ip"

    for proxy in proxies:
        proxy_url = proxy.get_proxy_url()
        if await test_proxy_connection(proxy_url, test_url):
            working_proxies.append(proxy)
        else:
            logger.warning(f"❌ Прокси {proxy.host}:{proxy.port} не прошел тест")

    logger.info(f"📊 Рабочих прокси: {len(working_proxies)}/{len(proxies)}")
    return working_proxies


def get_random_user_agent() -> str:
    """Возвращает случайный User-Agent"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]
    return random.choice(user_agents)


def build_api_url(vacancy_id: str) -> str:
    """Строит URL для API запроса к hh.ru"""
    return f"https://api.hh.ru/vacancies/{vacancy_id}"


async def create_http_session() -> aiohttp.ClientSession:
    """
    Создает асинхронную HTTP сессию для одного соединения
    """
    timeout = aiohttp.ClientTimeout(total=45, connect=15, sock_read=25)

    session = aiohttp.ClientSession(
        timeout=timeout,
        headers={
            "User-Agent": get_random_user_agent(),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://hh.ru/",
        },
    )

    return session


@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientError, asyncio.TimeoutError, ConnectionError, OSError),
    max_tries=3,
    max_time=60,
)
async def check_single_vacancy(vacancy_id: str, proxy: ProxyConfig) -> Union[str, bool]:
    """
    Проверяет одну вакансию через hh.ru API с использованием конкретного прокси
    """
    start_time = time.time()
    api_url = build_api_url(vacancy_id)
    proxy_url = proxy.get_proxy_url()

    # Создаем отдельную сессию для этого запроса
    session = await create_http_session()

    try:
        async with session.get(api_url, proxy=proxy_url, ssl=False) as response:
            response_time = time.time() - start_time

            if response.status == 404:
                logger.info(
                    f"✅ Вакансия {vacancy_id} закрыта (404). Время: {response_time:.2f}с. Прокси: {proxy.host}:{proxy.port}"
                )
                return vacancy_id

            elif response.status == 200:
                logger.info(
                    f"❌ Вакансия {vacancy_id} активна. Время: {response_time:.2f}с. Прокси: {proxy.host}:{proxy.port}"
                )
                return False

            elif response.status == 403:
                error_text = await response.text()
                raise aiohttp.ClientError(
                    f"Доступ запрещен (403). Прокси: {proxy.host}:{proxy.port}. Ответ: {error_text}"
                )

            elif response.status == 429:
                retry_after = response.headers.get("Retry-After", 10)
                logger.warning(
                    f"⚠️ Превышен лимит запросов для {vacancy_id}. Ждем {retry_after}сек. Прокси: {proxy.host}:{proxy.port}"
                )
                await asyncio.sleep(int(retry_after))
                response.raise_for_status()

            else:
                error_text = await response.text()
                raise aiohttp.ClientError(
                    f"HTTP {response.status}. Прокси: {proxy.host}:{proxy.port}. Ответ: {error_text}"
                )

    except aiohttp.ClientResponseError as e:
        response_time = time.time() - start_time
        if e.status == 404:
            logger.info(
                f"✅ Вакансия {vacancy_id} закрыта (404). Время: {response_time:.2f}с. Прокси: {proxy.host}:{proxy.port}"
            )
            return vacancy_id
        raise

    except Exception as e:
        response_time = time.time() - start_time
        logger.warning(
            f"⚠️ Ошибка при проверке {vacancy_id}. Время: {response_time:.2f}с. Прокси: {proxy.host}:{proxy.port}. Ошибка: {str(e)}"
        )
        raise

    finally:
        # Всегда закрываем сессию
        await session.close()


async def process_single_vacancy(
    vacancy_id: str, proxy_manager: ProxyManager
) -> Union[str, bool, None]:
    """
    Обрабатывает одну вакансию с гарантией 1 соединение на прокси
    """
    proxy = None
    try:
        # Ждем свободный прокси
        while proxy is None:
            proxy = await proxy_manager.get_proxy()
            if proxy is None:
                await asyncio.sleep(0.1)
                continue

        # Добавляем небольшую случайную задержку
        delay = random.uniform(0.1, 0.3)
        await asyncio.sleep(delay)

        # Проверяем вакансию
        return await check_single_vacancy(vacancy_id, proxy)

    except Exception as e:
        logger.error(
            f"🚨 Все попытки проверки вакансии {vacancy_id} не удались. Ошибка: {str(e)}"
        )
        return None

    finally:
        # Всегда освобождаем прокси
        if proxy:
            await proxy_manager.release_proxy(proxy)


async def check_vacancies_batch(
    vacancy_ids: List[str], proxies: List[ProxyConfig], test_proxies: bool = True
) -> List[Union[str, bool, None]]:
    """
    Основная функция для проверки пачки вакансий
    с ограничением 1 соединение на прокси
    """
    logger.info(f"🚀 Начинаем проверку {len(vacancy_ids)} вакансий")

    # Тестируем прокси перед использованием
    working_proxies = proxies
    if test_proxies:
        working_proxies = await test_all_proxies(proxies)
        if not working_proxies:
            raise ValueError("❌ Нет рабочих прокси!")
        logger.info(f"🔄 Используем {len(working_proxies)} рабочих прокси")
    else:
        logger.info(f"🔄 Используем {len(working_proxies)} прокси (без тестирования)")

    # Создаем менеджер прокси
    proxy_manager = ProxyManager(working_proxies)

    # Создаем задачи для всех вакансий
    tasks = [
        process_single_vacancy(vacancy_id, proxy_manager) for vacancy_id in vacancy_ids
    ]

    # Выполняем все задачи
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Обрабатываем результаты
    processed_results = []
    for i, result in enumerate(results):
        vacancy_id = vacancy_ids[i]
        if isinstance(result, Exception):
            logger.error(
                f"🚨 Необработанное исключение для {vacancy_id}: {str(result)}"
            )
            processed_results.append(None)
        else:
            processed_results.append(result)

    return processed_results


async def main():
    """
    Пример использования с ограничением 1 соединение на прокси
    """
    # Ваша конфигурация HTTP прокси
    your_proxy_config = [
        {
            "host": "188.130.221.39",
            "port": 3000,  # Обычно порт 8080, 3128, 1080 для HTTP прокси
            "username": "z9L5Ny54",
            "password": "h78KuOKh",
        },
        {
            "host": "31.40.203.85",
            "port": 3000,
            "username": "z9L5Ny54",
            "password": "h78KuOKh",
        },
        {
            "host": "170.168.137.171",
            "port": 8000,
            "username": "Cub1tG",
            "password": "gGXRbk",
        },
        {
            "host": "185.240.92.8",
            "port": 8000,
            "username": "tBNwAT",
            "password": "6Fqcwf",
        },
        # Добавьте столько прокси, сколько у вас есть
        # Каждый прокси будет обрабатывать 1 запрос одновременно
    ]

    # Загружаем прокси
    proxies = load_proxies_from_config(your_proxy_config)

    # ID вакансий для проверки
    vacancy_ids = get_open_vacancies_links()

    try:
        # Проверяем вакансии
        results = await check_vacancies_batch(
            vacancy_ids=vacancy_ids, proxies=proxies, test_proxies=True
        )

        # Статистика
        total = len(results)
        closed = sum(1 for r in results if isinstance(r, str))
        active = sum(1 for r in results if r is False)
        errors = sum(1 for r in results if r is None)

        print(f"\n📊 Результаты:")
        print(f"Всего проверено: {total}")
        print(f"Закрытых: {closed} ({closed / total * 100:.1f}%)")
        print(f"Активных: {active} ({active / total * 100:.1f}%)")
        print(f"Ошибок: {errors} ({errors / total * 100:.1f}%)")

        # Показываем закрытые вакансии
        closed_ids = [r for r in results if isinstance(r, str)]
        if closed_ids:
            print(f"Закрытые ID: {', '.join(closed_ids)}")

        return results

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        return []


if __name__ == "__main__":
    asyncio.run(main())
