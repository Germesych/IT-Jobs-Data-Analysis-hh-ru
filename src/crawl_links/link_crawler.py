from bs4 import BeautifulSoup
from src.crawl_links.main_requests import fetch_vacancy_data
import csv
from datetime import datetime
from urllib.parse import urlparse
from src.database.db_manager import save_data_to_sqlite
from src.utils.main_logger import setup_logger

# Инициализация логгера для текущего модуля
logger = setup_logger(__name__)


def get_link_id(url):
    """Извлекает ID вакансии из URL.

    Args:
        url (str): URL вакансии

    Returns:
        str: ID вакансии (последняя часть пути URL)
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    vacancy_id = path_parts[-1]
    # print('get_link_id: ', vacancy_id)
    return vacancy_id


def add_to_csv(data):
    """Добавляет данные вакансии в CSV файл.

    Если файл не существует, создает его и записывает заголовки.
    Если файл существует, добавляет данные в конец файла.

    Args:
        data (dict): Словарь с данными вакансии для записи
    """
    # Имя файла
    csv_file = 'vacancies.csv'

    # Проверяем, существует ли файл, чтобы записать заголовки при первом запуске
    file_exists = False
    try:
        with open(csv_file, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    # Открываем файл в режиме добавления
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())

        # Записываем заголовки, если файл новый
        if not file_exists:
            writer.writeheader()

        # Добавляем новую строку
        writer.writerow(data)


def vacancy_close(res_data):
    """
    Формирует данные о закрытой вакансии для записи.

    Args:
        res_data (dict): Данные ответа от API

    Returns:
        dict: Словарь с ID вакансии и датой закрытия
    """
    link_id = get_link_id(res_data['url'])
    return {
        'id': link_id,
        'date': datetime.now().isoformat(),
    }


def read_links_from_file(file_path: str) -> list[str]:
    """Читает ссылки из файла и возвращает их в виде списка.

    Args:
        file_path (str): Путь к файлу со ссылками

    Returns:
        list[str]: Список ссылок на вакансии
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        links = [line.strip() for line in file if line.strip()]
    return links


def get_country_from_filename(filename: str) -> str:
    """Извлекает код страны из начала имени файла и возвращает название страны.

    Args:
        filename (str): Имя файла, например, '16_vacancies_links.txt'.

    Returns:
        str: Название страны ('Беларусь' или 'Россия') или 'Неизвестно'.
    """
    country_code = filename.split('_')[0]

    if country_code == "16":
        return "Беларусь"
    elif country_code == "113":
        return "Россия"
    else:
        return "Неизвестно"


def crawl_links(url: str | bool, file_path: str) -> None:
    """Основная функция для обработки ссылок на вакансии.

    Если url не указан, читает ссылки из файла 'vacancies_links.txt'.
    Если url указан, обрабатывает только эту ссылку.

    Args:
        url (str or bool): URL для обработки или False для чтения из файла
    """

    country = get_country_from_filename(file_path)

    if not url:
        urls = read_links_from_file(file_path)

        for link in urls:
            main(link, country)
    else:
        main(url, country)


# Тестовый URL для отладки
test_url = "https://api.hh.ru/vacancies/124953065?host=hh.ru"


def safe_get(d, *keys, default=None):
    """Безопасно получает значение по цепочке ключей из словаря.

    Args:
        d (dict): Словарь для поиска
        *keys: Цепочка ключей для последовательного доступа
        default: Значение по умолчанию, если ключ не найден

    Returns:
        Значение по указанным ключам или default если ключ не найден
    """
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d


def main(link: str, country: str) -> None:
    """Основная функция обработки вакансии.

    Получает данные вакансии по API, парсит и сохраняет в CSV.

    Args:
        link (str): URL вакансии для обработки
    """
    # Получаем данные вакансии через API
    data = fetch_vacancy_data(link)

    if not data:
        print("Ошибка: не удалось получить данные.")
        return

    # Проверяем, закрыта ли вакансия
    if data.get('closed'):
        logger.info(f"vacancy is closed! url: {data.get('url')}")
        return
    
    # Обработка зарплатных ожиданий
    sr = data.get("salary_range") or {}
    mode = sr.get("mode") or {}                 # то же самое для mode
    freq = sr.get("frequency") or {}

    # Обрабатываем адрес вакансии
    address_data = data.get('address')
    address = address_data.get('raw') if isinstance(address_data,
                                                    dict) else address_data if address_data is not None else None

    # professional_roles_name
    roles = data.get("professional_roles") or []
    if not roles:
        professional_roles_name = None
    else:
        professional_roles_name = roles[0].get("name")

    # work_format
    work_format = data.get('schedule') or {}
    if not work_format:
        work_format_data = None
    else:
        work_format_data = work_format.get('name')

    # work_schedule_by_days
    employment = data.get('employment') or {}
    if not employment:
        employment_data = None
    else:
        employment_data = employment.get('name')

    # company_accredited_it_employerl
    company_employer = data.get('employer') or None
    if not company_employer:
        company_accredited = False
    else:
        company_accredited = company_employer.get('accredited_it_employer')


    # Формируем структурированные данные вакансии
    vacancy_data = {
        'id': data.get('id'),
        'country': country or None,
        'site': 'hh_ru',
        'title': data.get('name'),
        'salary_from': sr.get("from"),
        'salary_to': sr.get("to"),
        'currency': sr.get("currency"),
        'mode_name': mode.get("name"),
        'frequency_name': freq.get("name"),
        'city': safe_get(data, 'area', 'name'),
        'address': address,
        'experience': safe_get(data, 'experience', 'name'),
        'schedule': safe_get(data, 'schedule', 'name'),
        'employment': safe_get(data, 'employment', 'name'),
        'description': BeautifulSoup(data.get('description', ''), 'html.parser').get_text() if data.get('description') else '',
        'skills': [skill['name'] for skill in data.get('key_skills', [])],
        'professional_roles_name': professional_roles_name,
        'company_id': safe_get(data, 'employer', 'id'),
        'company_name': safe_get(data, 'employer', 'name'),
        'company_url': safe_get(data, 'employer', 'url'),
        'company_vacancies_url': safe_get(data, 'employer', 'vacancies_url'),
        'company_accredited_it_employerl': company_accredited,
        'published_at': data.get('published_at'),
        'created_at': data.get('created_at'),
        'employment_form': safe_get(data, 'employment', 'name'),
        'work_format': work_format_data,
        'work_schedule_by_days': employment_data,
        'vacancy_close_date': None,
    }

    # Добавляем данные в CSV файл
    add_to_csv(vacancy_data)
    save_data_to_sqlite(vacancy_data)

    # Выводим данные для отладки
    # print(vacancy_data)
    print('Vacancie add!')


if __name__ == "__main__":
    # Точка входа - запуск обработки тестового URL
    # crawl_links(test_url, '16_vacancies_links.txt')
    # crawl_links(test_url, '113_vacancies_links.txt')

    # Обработка ссылок из файла для Беларуси
    crawl_links(False, '16_vacancies_links.txt')
    # Обработка ссылок из файла для России
    crawl_links(False, '113_vacancies_links.txt')
