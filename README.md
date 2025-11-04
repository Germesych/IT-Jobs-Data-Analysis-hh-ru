Установка пакетов из requirements.txt

```bash
pip install -r requirements.txt
```

Если вы хотите убедиться, что пакеты обновлены до последней версии, можно использовать:

```bash
pip install --upgrade -r requirements.txt
```

Эта команда сохранит список установленных пакетов в файл requirements.txt

```bash
pip freeze > requirements.txt
```

```python
# parser_hh/src/crawl_links/link_crawler.py
# Формируем структурированные данные вакансии
    vacancy_data = {
        'id': data.get('id'),
        'country': country or None,
        'site': 'hh_ru',
        'title': data.get('name'),
        'citi': safe_get(data, 'area', 'name'),
        'address': address,
        'experience': safe_get(data, 'experience', 'name'),
        'schedule': safe_get(data, 'schedule', 'name'),
        'employment': safe_get(data, 'employment', 'name'),
        'description': BeautifulSoup(data.get('description', ''), 'html.parser').get_text() if data.get(
            'description') else '',
        'skills': [skill['name'] for skill in data.get('key_skills', [])],
        'professional_roles_id': safe_get(data, 'professional_roles', 0, 'id') if data.get(
            'professional_roles') else None,
        'professional_roles_name': safe_get(data, 'professional_roles', 0, 'name') if data.get(
            'professional_roles') else None,
        'company_id': safe_get(data, 'employer', 'id'),
        'company_name': safe_get(data, 'employer', 'name'),
        'company_url': safe_get(data, 'employer', 'url'),
        'company_vacancies_url': safe_get(data, 'employer', 'vacancies_url'),
        'company_accredited_it_employerl': 'False' if safe_get(data, 'employer',
                                                               'accredited_it_employer') is None else str(
            safe_get(data, 'employer', 'accredited_it_employer')),
        'published_at': data.get('published_at'),
        'created_at': data.get('created_at'),
        'languages_id': safe_get(data, 'languages', 0, 'id') if data.get('languages') else None,
        'languages_name': safe_get(data, 'languages', 0, 'name') if data.get('languages') else None,
        'languages_level': safe_get(data, 'languages', 0, 'level', 'name') if data.get('languages') else None,
        'employment_form': safe_get(data, 'employment', 'name'),
        'work_format': safe_get(data, 'work_format', 0, 'name', default='').replace('\xa0', ' ') if data.get(
            'work_format') else '',
        'work_schedule_by_days': safe_get(data, 'work_schedule_by_days', 0, 'name') if data.get(
            'work_schedule_by_days') else None,
        'working_hours': safe_get(data, 'working_hours', 0, 'name', default='').replace('\xa0', ' ') if data.get(
            'working_hours') else '',
        'salary_from'=salary_block.get('from'),
        'salary_to'=salary_block.get('to'),
        'currency'=salary_block.get('currency'),
        'mode_name'=safe_get(salary_block, 'mode', 'name'),
        'frequency_name'=safe_get(salary_block, 'frequency', 'name'),
        'vacancy_close_date': None,
    }
```

salary_range: {
from: 80000,
to: 150000,
currency: "RUR",
gross: false,
mode: {2 entries
id: "MONTH",
name: "За месяц"
},
frequency: {2 entries
id: "TWICE_PER_MONTH",
name: "Два раза в месяц"
}
},

salary_from
salary_to
currency
mode_name
frequency_name


```python
from src.database.db_manager import get_open_vacancies_links
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
```
