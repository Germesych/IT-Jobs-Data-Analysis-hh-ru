# Документация для парсера вакансий hh.ru

## Обзор
Этот модуль парсит данные о вакансиях с hh.ru по API, обрабатывает их и сохраняет в CSV-файл. Включает функции для извлечения ID из URL, безопасного доступа к вложенным данным, обработки HTML и логирования.

## Функции

### `get_link_id(url)`
```python
def get_link_id(url):
    """
    Извлекает ID вакансии из URL.

    Args:
        url (str): URL вакансии (например, 'https://api.hh.ru/vacancies/124591522?host=hh.ru').

    Returns:
        str: ID вакансии (например, '124591522').

    Example:
        >>> get_link_id('https://api.hh.ru/vacancies/124591522?host=hh.ru')
        '124591522'
    """
```

### `add_to_csv(data)`
```python
def add_to_csv(data):
    """
    Добавляет данные вакансии в CSV-файл 'vacancies.csv'.
    Автоматически записывает заголовки при первом запуске.

    Args:
        data (dict): Словарь с данными вакансии (ключи = названия столбцов CSV).

    Note:
        - Использует UTF-8 кодировку.
        - Добавление данных в конец файла (режим 'a').
    """
```

### `vacancy_close(res_data)`
```python
def vacancy_close(res_data):
    """
    Обрабатывает данные закрытой вакансии.

    Args:
        res_data (dict): Данные вакансии с ключом 'url'.

    Returns:
        dict: Словарь с ID вакансии и текущей датой/временем.
    """
```

### `read_links_from_file(file_path)`
```python
def read_links_from_file(file_path: str) -> list[str]:
    """
    Читает список ссылок на вакансии из текстового файла.

    Args:
        file_path (str): Путь к файлу со ссылками (по одной на строку).

    Returns:
        list[str]: Список URL вакансий.

    Example:
        Файл 'vacancies_links.txt':
        https://api.hh.ru/vacancies/124591522?host=hh.ru
        https://api.hh.ru/vacancies/125336631?host=hh.ru

        >>> read_links_from_file('vacancies_links.txt')
        ['https://api.hh.ru/vacancies/124591522?host=hh.ru', ...]
    """
```

### `crawl_links(url=False)`
```python
def crawl_links(url=False):
    """
    Основная функция парсинга. Обрабатывает одну ссылку или список из файла.

    Args:
        url (str, optional): URL одной вакансии. Если не указан, берёт список из 'vacancies_links.txt'.
    """
```

### `safe_get(d, *keys, default=None)`
```python
def safe_get(d, *keys, default=None):
    """
    Безопасно получает значение по цепочке ключей в словаре.

    Args:
        d (dict): Исходный словарь.
        *keys: Цепочка вложенных ключей.
        default: Значение по умолчанию при отсутствии ключа.

    Returns:
        Значение по ключам или default.

    Example:
        >>> data = {'a': {'b': {'c': 1}}}
        >>> safe_get(data, 'a', 'b', 'c')
        1
        >>> safe_get(data, 'x', 'y') is None
        True
    """
```

### `main(link)`
```python
def main(link) -> None:
    """
    Обрабатывает данные одной вакансии и сохраняет их в CSV.

    Args:
        link (str): URL вакансии.

    Process:
        1. Получает данные через API (fetch_vacancy_data).
        2. Извлекает нужные поля (ID, заголовок, адрес и т.д.).
        3. Очищает HTML из описания (BeautifulSoup).
        4. Сохраняет данные в 'vacancies.csv'.
    """
```

## Структура данных
Парсер сохраняет следующие поля вакансии:

| Поле                       | Тип       | Описание                                  |
|----------------------------|-----------|------------------------------------------|
| id                         | str       | Уникальный идентификатор вакансии        |
| site                       | str       | Постоянное значение 'hh_ru'               |
| title                      | str       | Название вакансии                        |
| citi                       | str       | Город                                     |
| address                    | str       | Полный адрес                              |
| experience                 | str       | Требуемый опыт (например, '1-3 года')     |
| schedule                   | str       | График работы (например, 'Полный день')   |
| employment                 | str       | Тип занятости                            |
| description                | str       | Текст описания (без HTML)                |
| skills                     | list[str] | Список ключевых навыков                  |
| professional_roles_id      | str       | ID профессиональной роли                 |
| professional_roles_name    | str       | Название роли                            |
| company_id                 | str       | ID работодателя                          |
| company_name               | str       | Название компании                        |
| company_url                | str       | Ссылка на сайт компании                  |
| company_vacancies_url      | str       | Ссылка на вакансии компании              |
| company_accredited_it_employerl | bool | Флаг аккредитованного IT-работодателя  |
| published_at               | str       | Дата публикации                          |
| created_at                 | str       | Дата создания                            |
| languages_id               | str       | ID языка (например, 'eng')               |
| languages_name             | str       | Название языка                           |
| languages_level            | str       | Уровень владения (например, 'B2')        |
| employment_form            | str       | Форма занятости                          |
| work_format                | str       | Формат работы (например, 'Удалённо')     |
| work_schedule_by_days      | str       | График (например, '5/2')                 |
| working_hours              | str       | Режим рабочего времени                   |
| vacancy_close_date         | None      | Зарезервировано для будущего использования |

## Использование

### Пример запуска для одной вакансии:
```python
crawl_links('https://api.hh.ru/vacancies/124953065?host=hh.ru')
```

### Пример запуска для списка из файла:
1. Создайте файл `vacancies_links.txt` с URL (по одному на строку).
2. Вызовите:
```python
crawl_links()
```

## Зависимости
- `BeautifulSoup` (parsing HTML)
- `csv` (работа с CSV)
- `urllib.parse` (парсинг URL)
- Внешний модуль `fetch_vacancy_data` из `src.crawl_links.main_requests`

## Логирование
Используется логгер из `src.utils.main_logger` для записи сообщений об ошибках и закрытых вакансиях.

## Примечания
- Файл `vacancies.csv` создаётся автоматически при первом запуске.
- Для работы требуется файл `vacancies_links.txt` с URL вакансий (если не указан конкретный URL).
- Кодировка CSV и текстовых файлов: UTF-8.