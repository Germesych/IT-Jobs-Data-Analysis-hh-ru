"""Модуль для работы с API вакансий: получение метаданных и параметров поиска."""

from typing import List, Dict, Any
import requests
from dataclasses import dataclass
from src.utils.fetch_vacancies import fetch_vacancies_data
from src.models.vacancy_search_params import VacancySearchParams
from src.utils.main_logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class VacanciesMetadata:
    """Метаданные о результатах поиска вакансий.

    Attributes:
        vacancies (List[Dict[str, Any]]): Список вакансий. Каждая вакансия — словарь с полями:
            - id (str): Идентификатор вакансии.
            - name (str): Название вакансии.
            - url (str): Ссылка на вакансию на сайте.
            - alternate_url (str): Ссылка на вакансию в API.
            - salary (Optional[Dict[str, Any]]): Информация о зарплате (может отсутствовать).
            - ... и другие поля, возвращаемые API.
        found (int): Общее количество найденных вакансий.
        pages (int): Общее количество страниц с вакансиями.
        page (int): Текущая страница.
        per_page (int): Количество вакансий на странице.

    Examples:
        >>> metadata = VacanciesMetadata(
        ...     vacancies=[{"id": "123", "name": "Python Developer", "url": "https://hh.ru/vacancy/123"}],
        ...     found=100,
        ...     pages=5,
        ...     page=0,
        ...     per_page=20
        ... )
        >>> print(metadata.vacancies[0]["name"])
        Python Developer
    """

    vacancies: List[Dict[str, Any]]
    found: int
    pages: int
    page: int
    per_page: int

def get_vacancies_metadata(params: VacancySearchParams) -> Dict[str, Any] | None:
    """Получает метаданные о вакансиях по заданным параметрам поиска.

    Args:
        params (VacancySearchParams): Объект с параметрами поиска вакансий.
            Пример:
                VacancySearchParams(area=16, professional_role=96, page=0)

    Returns:
        Dict[str, Any]: Словарь с метаданными и списком вакансий.
            Ключи:
                vacancies (List[Dict[str, Any]]): Список вакансий.
                found (int): Общее количество вакансий.
                pages (int): Количество страниц.
                page (int): Текущая страница.
                per_page (int): Количество вакансий на странице.

    Raises:
        requests.exceptions.RequestException: Ошибка при выполнении HTTP-запроса.
        ValueError: Ошибка декодирования JSON-ответа.
        Exception: Неожиданная ошибка.

    Examples:
        >>> from src.models.vacancy_search_params import VacancySearchParams
        >>> metadata = get_vacancies_metadata(VacancySearchParams())
        >>> print(f"Найдено {metadata['found']} вакансий на {metadata['pages']} страницах.")
        Найдено 904 вакансий на 10 страницах.

        >>> # Поиск вакансий в Беларуси (area=16) для категории IT (professional_role=96)
        >>> params = VacancySearchParams(area=16, professional_role=96, page=0)
        >>> metadata = get_vacancies_metadata(params)
        >>> for vacancy in metadata['vacancies'][:3]:  # Первые 3 вакансии
        ...     print(f"{vacancy['name']} (Зарплата: {vacancy.get('salary', 'не указана')})")
        Python Developer (Зарплата: от 3000 BYN)
        DevOps Engineer (Зарплата: не указана)
        Data Scientist (Зарплата: {'from': 4000, 'currency': 'BYN'})

        >>> # Получение вакансий по конкретной странице
        >>> params = VacancySearchParams(area=113, professional_role=96, page=1)
        >>> metadata = get_vacancies_metadata(params)
        >>> print(f"URL запроса: {metadata['url']}")
        URL запроса: https://api.hh.ru/vacancies?area=113&professional_role=96&page=1&...

        >>> # Работа с вакансиями
        >>> metadata = get_vacancies_metadata(VacancySearchParams(per_page=5))
        >>> vacancies = metadata['vacancies']
        >>> print(f"Первая вакансия: {vacancies[0]['name']} (ID: {vacancies[0]['id']})")
        Первая вакансия: Middle Python Developer (ID: 125572095)
    """
    try:
        fetch_data = fetch_vacancies_data(params=params)
        request_url = fetch_data['url']

        data = VacanciesMetadata(
            vacancies=fetch_data['data']['items'],
            found=fetch_data['data']['found'],
            pages=fetch_data['data']['pages'],
            page=fetch_data['data']['page'],
            per_page=fetch_data['data']['per_page']
        ).__dict__

        # logger.info(f"get_vacancies_metadata: {data}")
        logger.info(f"get_vacancies_metadata URL: {request_url}")

        return data

    except requests.exceptions.RequestException as err:
        logger.error(f"Не удалось получить данные: {err}")
        raise

    except ValueError as err:
        logger.error(f"Ошибка обработки данных: {err}")
        raise

    except Exception as err:
        logger.error(f"Неожиданная ошибка: {err}")
        raise

if __name__ == "__main__":
    try:
        # Пример 1: Получение вакансий с параметрами по умолчанию
        metadata = get_vacancies_metadata(VacancySearchParams())
        logger.debug(f"Найдено {metadata['found']} вакансий на {metadata['pages']} страницах.")

        # Пример 2: Вывод информации о первых 5 вакансиях
        for idx, vacancy in enumerate(metadata['vacancies'][:5], 1):
            logger.debug(f"{idx}. {vacancy['name']} (ID: {vacancy['id']})")

        # Пример 3: Получение URL запроса
        logger.debug(f"URL запроса: {metadata.get('url', 'отсутствует')}")

        # Пример 4: Пагинация
        logger.debug(f"Текущая страница: {metadata['page'] + 1} из {metadata['pages']}")

    except Exception as err:
        logger.error(f"Ошибка в основном блоке: {err}")
