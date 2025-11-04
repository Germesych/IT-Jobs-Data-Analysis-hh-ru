import httpx
import random
import time
from typing import Optional, Dict, Any
from src.utils.main_logger import setup_logger

# Инициализация логгера для записи сообщений об ошибках, предупреждений и отладочной информации.
logger = setup_logger(__name__)

# Список User-Agent для имитации запросов от разных браузеров, чтобы избежать блокировки.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

class RateLimiter:
    """
    Класс для ограничения частоты запросов к API.

    Атрибуты:
        calls_per_minute (int): Максимальное количество запросов в минуту.
        min_interval (float): Минимальный интервал между запросами в секундах.
        last_call_time (float): Время последнего запроса.
        request_counter (int): Счетчик выполненных запросов.
        initial_requests (int): Количество запросов без задержки в начале.
    """

    def __init__(self, calls_per_minute: int = 100, initial_requests: int = 3) -> None:
        """
        Инициализирует RateLimiter с заданным количеством запросов в минуту.

        Args:
            calls_per_minute (int): Количество запросов в минуту. По умолчанию 100.
            initial_requests (int): Количество запросов без задержки в начале. По умолчанию 3.
        """
        self.calls_per_minute = calls_per_minute
        self.min_interval = 60.0 / calls_per_minute
        self.last_call_time = 0
        self.request_counter = 0
        self.initial_requests = initial_requests

    def wait_if_needed(self) -> None:
        """
        Приостанавливает выполнение, если с момента последнего запроса прошло недостаточно времени.
        Первые initial_requests запросов выполняются без задержки.
        """
        self.request_counter += 1

        # Если это один из первых initial_requests запросов - пропускаем задержку
        if self.request_counter <= self.initial_requests:
            self.last_call_time = time.time()
            logger.debug(f"Запрос {self.request_counter}/{self.initial_requests} без задержки")
            return

        current_time = time.time()
        elapsed = current_time - self.last_call_time
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            logger.debug(f"Задержка {sleep_time:.2f} сек перед запросом {self.request_counter}")
            time.sleep(sleep_time)
        self.last_call_time = time.time()

# Глобальный экземпляр RateLimiter с безопасным лимитом запросов и 3 запросами без задержки
rate_limiter = RateLimiter(calls_per_minute=80, initial_requests=3)

def fetch_vacancy_data(
        url: str,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        timeout: float = 15.0,
) -> Optional[Dict[str, Any]]:
    """
    Выполняет синхронный запрос к API hh.ru с улучшенной обработкой ошибок и повторными попытками.

    Args:
        url (str): URL для запроса.
        max_retries (int): Максимальное количество попыток. По умолчанию 3.
        base_delay (float): Базовая задержка перед повторной попыткой. По умолчанию 1.0.
        max_delay (float): Максимальная задержка перед повторной попыткой. По умолчанию 30.0.
        timeout (float): Таймаут запроса. По умолчанию 15.0.

    Returns:
        Optional[Dict[str, Any]]: Данные вакансии или None в случае неудачи.
    """
    # Применяем ограничение частоты запросов перед каждым запросом
    rate_limiter.wait_if_needed()

    for attempt in range(max_retries):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate"
            }

            with httpx.Client(
                    timeout=timeout,
                    follow_redirects=True,
                    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            ) as client:
                response = client.get(url, headers=headers)

                # Обработка специфичных статусов
                if response.status_code == 404:
                    logger.info(f"Вакансия не найдена (404): {url}")
                    return {"closed": True, "url": url, "not_found": True}
                elif response.status_code == 410:
                    logger.info(f"Вакансия удалена (410): {url}")
                    return {"closed": True, "url": url, "gone": True}
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limit превышен, ждем {retry_after} сек: {url}")
                    time.sleep(min(retry_after, max_delay))
                    continue

                response.raise_for_status()
                data = response.json()
                logger.debug(f"Успешно получены данные: {url}")
                return data

        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code if e.response else "unknown"
            logger.warning(f"HTTP {status_code} для {url}. Попытка {attempt + 1}/{max_retries}")
            if status_code in [429, 503]:  # Too Many Requests, Service Unavailable
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
            else:
                delay = base_delay * (attempt + 1)
            if attempt < max_retries - 1:
                logger.info(f"Повтор через {delay:.1f} сек...")
                time.sleep(delay)
            continue

        except (httpx.ConnectError, httpx.ReadError, httpx.ConnectTimeout) as e:
            logger.warning(f"Сетевая ошибка ({type(e).__name__}): {url}. Попытка {attempt + 1}/{max_retries}")
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
            if attempt < max_retries - 1:
                time.sleep(delay)
            continue

        except httpx.TimeoutException:
            logger.warning(f"Таймаут для {url}. Попытка {attempt + 1}/{max_retries}")
            delay = min(base_delay * (2 ** attempt), max_delay)
            if attempt < max_retries - 1:
                time.sleep(delay)
            continue

        except Exception as e:
            logger.error(f"Неожиданная ошибка для {url}: {str(e)}")
            if attempt == max_retries - 1:
                return None
            time.sleep(base_delay)
            continue

    logger.error(f"Не удалось получить данные после {max_retries} попыток: {url}")
    return None
