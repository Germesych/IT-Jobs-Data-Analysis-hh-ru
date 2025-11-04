"""Модуль для работы с API hh.ru: получение данных о вакансиях с обработкой ошибок и повторными попытками."""

import requests
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.util.ssl_ import create_urllib3_context
from typing import Dict, Any, Optional
from src.models.vacancy_search_params import VacancySearchParams
from dotenv import load_dotenv
import os

# Logger
from src.utils.main_logger import setup_logger
logger = setup_logger(__name__)

# Загрузка URL из .env (например, 'https://api.hh.ru/vacancies')
load_dotenv()
URL = os.getenv('URL', 'https://api.hh.ru/vacancies')

# Список User-Agent для ротации (имитация различных браузеров)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def create_session() -> requests.Session:
    """Создаёт HTTP-сессию с настройками повторных попыток и современным TLS 1.2.

    Features:
        - Автоматическое повторение запросов при временных ошибках (5xx, 429).
        - Современный TLS 1.2 для совместимости с серверами.
        - Повторное использование соединений для повышения производительности.

    Returns:
        requests.Session: Настроенная HTTP-сессия.
    """
    session = requests.Session()

    # Настройка стратегии повторных попыток:
    # - 3 попытки по умолчанию
    # - Экспоненциальная задержка (1s, 2s, 4s, ...)
    # - Повтор при статусах 429, 500, 502, 503, 504
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )

    # Кастомный адаптер для настройки TLS 1.2
    class TLSAdapter(HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            context = create_urllib3_context(ssl_version="TLSv1_2")
            kwargs["ssl_context"] = context
            return super().init_poolmanager(*args, **kwargs)

    adapter = TLSAdapter()
    session.mount("https://", adapter)
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    return session

def fetch_vacancies_data(
    url: str = URL,
    params: Optional[VacancySearchParams] = None,
    timeout: int = 10,
    retry_on_403: bool = True,
    max_retries_on_403: int = 2,
) -> Dict[str, Any] | None:
    """Выполняет GET-запрос к API hh.ru с обработкой ошибок и повторными попытками.

    Args:
        url (str): URL API. По умолчанию берётся из переменной окружения `URL`.
        params (Optional[VacancySearchParams]): Параметры запроса (например, `area`, `professional_role`).
        timeout (int): Таймаут запроса в секундах. По умолчанию: 10.
        retry_on_403 (bool): Повторять запрос при ошибке 403 Forbidden. По умолчанию: True.
        max_retries_on_403 (int): Макс. количество повторов при 403. По умолчанию: 2.

    Returns:
        Dict[str, Any]: Словарь с данными вакансий, включая:
            - items (List[Dict]): Список вакансий.
            - data (Dict): Полный ответ API.
            - url (str): Финальный URL запроса.

    Raises:
        requests.exceptions.RequestException: Если все попытки завершились ошибкой.
        ValueError: Если ответ не является корректным JSON.

    Examples:
        >>> # Получение списка вакансий в Беларуси (area=16)
        >>> params = VacancySearchParams(area=16, per_page=2)
        >>> data = fetch_vacancies_data(params=params)
        >>> print(f"Найдено {len(data['items'])} вакансий")

        >>> # Получение одной вакансии по ID
        >>> vacancy = fetch_vacancies_data(url="https://api.hh.ru/vacancies/123456")
    """
    session = create_session()
    headers = {
        "User-Agent": random.choice(USER_AGENTS),  # Ротация User-Agent
        "Referer": "https://hh.ru",  # Имитация перехода с сайта hh.ru
    }
    request_params = params.__dict__ if params else {}

    for attempt in range(max_retries_on_403 + 1):  # +1 для первой попытки
        try:
            logger.info(f"Попытка {attempt + 1}/{max_retries_on_403 + 1}: {request_params}")
            response = session.get(url, params=request_params, headers=headers, timeout=timeout)
            logger.info(f"Сформированный URL: {response.url}")

            # Обработка 403 Forbidden
            if response.status_code == 403 and retry_on_403:
                logger.warning(f"403 Forbidden. Попытка {attempt + 1}/{max_retries_on_403 + 1}")
                if attempt < max_retries_on_403:
                    time.sleep(2 ** attempt)  # Экспоненциальная задержка: 1s, 2s, 4s, ...
                    continue
                else:
                    response.raise_for_status()  # Выбросить ошибку, если превышено количество попыток

            response.raise_for_status()  # Выбросить ошибку для других статусов (4xx, 5xx)
            response_data = response.json()

            vacancies_count = len(response_data.get('items', []))
            logger.debug(f"Получено {vacancies_count} вакансий")

            return {
                'items': response_data.get('items', []),
                'data': response_data,
                'url': response.url
            }

        except requests.exceptions.SSLError as err:
            logger.error(f"SSL Error: {err}. Проверьте настройки TLS и системное время.")
            raise

        except requests.exceptions.RequestException as err:
            logger.error(f"Ошибка при выполнении запроса: {err}")
            raise

        except ValueError as err:
            logger.error(f"Ошибка декодирования JSON: {err}")
            raise

def fetch_page_data(
    country: int,
    category: int,
    page: int,
    delay: float = 1.0
) -> Optional[Dict[str, Any]]:
    """Получает данные для одной страницы вакансий с задержкой между запросами.

    Args:
        country (int): ID региона (например, 113 для России, 16 для Беларуси).
        category (int): ID категории (профессиональной роли).
        page (int): Номер страницы.
        delay (float): Задержка перед запросом в секундах. По умолчанию: 1.0.

    Returns:
        Optional[Dict[str, Any]]: Данные страницы или None при ошибке.

    Example:
        >>> # Получение первой страницы вакансий IT в России
        >>> data = fetch_page_data(country=113, category=96, page=0)
    """
    time.sleep(delay)  # Задержка для снижения нагрузки на API
    params = VacancySearchParams(area=country, professional_role=category, page=page)
    try:
        return fetch_vacancies_data(params=params)
    except requests.exceptions.RequestException as err:
        logger.error(f"Ошибка на странице {page}: {err}")
        return None

if __name__ == "__main__":
    try:
        # Пример 1: Получение списка вакансий (первые 2 вакансии в Беларуси)
        params = VacancySearchParams(area=16, per_page=2)
        data = fetch_vacancies_data(params=params)
        logger.debug(f"Первая вакансия: {data['items'][0]['name'] if data['items'] else 'Нет данных'}")

        # Пример 2: Получение одной вакансии по ID
        vacancy_data = fetch_vacancies_data(url="https://api.hh.ru/vacancies/125436763")
        logger.debug(f"Вакансия: {vacancy_data['data']['name']}")

    except Exception as err:
        logger.error(f"Фатальная ошибка: {err}")
