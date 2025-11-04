from src.utils.random_delay import random_delay
from src.models.vacancy_search_params import VacancySearchParams
from src.parser.get_vacancies_metadata import get_vacancies_metadata
from src.utils.main_logger import setup_logger

logger = setup_logger(__name__)
found = 0  # Глобальная переменная для подсчёта общего количества найденных вакансий

def clear_file(filename: str) -> None:
    """
    Очищает содержимое файла. Если файл не существует, он будет создан.

    Args:
        filename (str): Путь к файлу.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('')
        logger.info(f"Файл {filename} успешно очищен.")
        print(f"Файл {filename} успешно очищен.")
    except PermissionError:
        logger.error(f"Ошибка: Нет прав на запись в файл {filename}.")
    except IsADirectoryError:
        logger.error(f"Ошибка: {filename} — это директория, а не файл.")
    except Exception as err:
        logger.error(f"Неожиданная ошибка при очистке файла {filename}: {err}")


def categories_manager(country: int):
    """
    Управляет категориями вакансий для заданной страны.

    Args:
        country (int): Идентификатор страны для поиска вакансий.
    """
    global found
    # Идентификаторы категорий профессий
    categories: tuple[int, ...] = (156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155, 96, 164, 104, 157, 107, 112, 113, 148, 114, 116, 121,
                  124, 125, 126,)
    for category in categories:
        # Создаём параметры поиска для текущей категории
        pages_params = VacancySearchParams(area=country, professional_role=category)
        metadata = get_vacancies_metadata(pages_params)
        pages = metadata["pages"]
        found += metadata["found"]
        fetch_page_data(country, category, pages)
        random_delay(min_seconds=1.0, max_seconds=2.0)  # Задержка для избежания блокировки

def fetch_page_data(country: int, category: int, pages: int):
    """
    Получает данные по страницам для заданной категории и страны.

    Args:
        country (int): Идентификатор страны.
        category (int): Идентификатор категории профессий.
        pages (int): Количество страниц для обработки.
    """
    page = 0
    for _ in range(pages):
        params = VacancySearchParams(area=country, professional_role=category, page=page)
        metadata = get_vacancies_metadata(params)
        get_urls_from_pages(metadata['vacancies'], country)
        page += 1
        print(f"fetch_page_data page+: {page}")
        random_delay(min_seconds=1.0, max_seconds=3.0)  # Задержка для избежания блокировки

def get_urls_from_pages(items: dict, country: int):
    """Извлекает URL из списка вакансий и записывает их в файл.

    Args:
        items (dict): Словарь, содержащий список вакансий.
    """
    try:
        for item in items:
            write_to_file(f'{country}_vacancies_links.txt', item['url'])
    except Exception as err:
        logger.error(f'Error get vacancy url {err}')

def write_to_file(filename: str, data: str) -> None:
    """
    Записывает строку в файл, сохраняя существующие данные.

    Args:
        filename (str): Путь к файлу.
        data (str): Строка для записи.
    """
    with open(filename, 'a', encoding='utf-8') as file:
        # print(f"\nWRITE LINK: {data}\n")
        file.write(data + '\n')  # Добавляем `\n` для перехода на новую строку

def parser_links():
    """
    Запускает процесс парсинга для двух стран.
    """
    clear_file('113_vacancies_links.txt')
    clear_file('16_vacancies_links.txt')
    categories_manager(113)  # Россия
    categories_manager(16)   # Беларусь

if __name__ == "__main__":
    parser_links()
    print(f"found: {found}")
