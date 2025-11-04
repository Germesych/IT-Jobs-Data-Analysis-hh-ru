import sqlite3
from datetime import datetime
from src.utils.main_logger import setup_logger

# Инициализация логера для текущего модуля
logger = setup_logger(__name__)


def get_db_connection():
    """Создает и возвращает подключение к базе данных"""
    return sqlite3.connect('vacancies.db')


# ---------- 1. Схема ----------
def initialize_database():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id TEXT PRIMARY KEY,
                country TEXT,
                site TEXT,
                title TEXT,
                city TEXT,
                address TEXT,
                experience TEXT,
                schedule TEXT,
                employment TEXT,
                description TEXT,
                skills TEXT,
                professional_roles_name TEXT,
                company_id TEXT,
                company_name TEXT,
                company_url TEXT,
                company_vacancies_url TEXT,
                company_accredited_it_employer TEXT,  -- Исправлено: убрана лишняя 'l'
                published_at TEXT,
                created_at TEXT,
                employment_form TEXT,
                work_format TEXT,
                work_schedule_by_days TEXT,
                vacancy_close_date TEXT,
                salary_from   INTEGER,
                salary_to     INTEGER,
                currency      TEXT,
                mode_name     TEXT,
                frequency_name TEXT
            )
        ''')
        conn.commit()
        logger.info("База данных инициализирована успешно")
    except Exception as err:
        logger.error(f"Ошибка при инициализации базы данных: {err}")
        raise
    finally:
        conn.close()


# ---------- 2. Вставка ----------
def insert_vacancy(vacancy_data: dict):
    """Вставляет или заменяет запись о вакансии в базе данных"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        skills_str = ', '.join(vacancy_data.get('skills', []))

        # 29 значений для 29 полей таблицы
        values = (
            vacancy_data.get('id'),
            vacancy_data.get('country'),
            vacancy_data.get('site'),
            vacancy_data.get('title'),
            vacancy_data.get('city'),
            vacancy_data.get('address'),
            vacancy_data.get('experience'),
            vacancy_data.get('schedule'),
            vacancy_data.get('employment'),
            vacancy_data.get('description'),
            skills_str,
            vacancy_data.get('professional_roles_name'),
            vacancy_data.get('company_id'),
            vacancy_data.get('company_name'),
            vacancy_data.get('company_url'),
            vacancy_data.get('company_vacancies_url'),
            vacancy_data.get('company_accredited_it_employer'),  # Исправлено
            vacancy_data.get('published_at'),
            vacancy_data.get('created_at'),
            vacancy_data.get('employment_form'),
            vacancy_data.get('work_format'),
            vacancy_data.get('work_schedule_by_days'), # Добавлено значение по умолчанию
            vacancy_data.get('vacancy_close_date'),
            vacancy_data.get('salary_from'),
            vacancy_data.get('salary_to'),
            vacancy_data.get('currency'),
            vacancy_data.get('mode_name'),
            vacancy_data.get('frequency_name')
        )

        cursor.execute('''
            INSERT OR REPLACE INTO vacancies (
                id, 
                country, 
                site, 
                title, 
                city, 
                address, 
                experience, 
                schedule,
                employment, 
                description, 
                skills,
                professional_roles_name, 
                company_id, 
                company_name, 
                company_url,
                company_vacancies_url, 
                company_accredited_it_employer,
                published_at, 
                created_at,
                employment_form, 
                work_format,
                work_schedule_by_days, 
                vacancy_close_date,
                salary_from, 
                salary_to, 
                currency,
                mode_name, 
                frequency_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', values)

        conn.commit()
        logger.info(f"Вакансия {vacancy_data.get('id')} успешно сохранена в базу данных")

    except Exception as err:
        logger.error(f"Ошибка при вставке данных: {err}")
        logger.error(f"Количество значений: {len(values)}")
        logger.error(f"Данные: {vacancy_data}")
        raise
    finally:
        conn.close()


def save_data_to_sqlite(data):  # Исправлено название функции
    """Сохраняет данные о вакансии в базу данных"""
    try:
        initialize_database()
        insert_vacancy(data)
        logger.info(f"Данные записаны успешно: {data['id']}")
    except Exception as err:
        logger.error(f"Ошибка при сохранении данных: {err}")
        raise


def get_total_vacancies():
    """Возвращает общее количество вакансий в базе данных"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM vacancies;')
        return cursor.fetchone()[0]
    finally:
        conn.close()


def get_today_vacancies_count():
    """Возвращает количество вакансий, созданных сегодня"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM vacancies WHERE created_at >= datetime("now", "start of day");')
        return cursor.fetchone()[0]
    finally:
        conn.close()


def get_last_vacancy():
    """Возвращает последнюю добавленную вакансию в виде словаря"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vacancies ORDER BY created_at DESC LIMIT 1;')
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    finally:
        conn.close()


def close_vacancy(vacancy_id):
    """Закрывает вакансию с текущей датой и временем"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        close_date = datetime.now().isoformat()

        cursor.execute('''
            UPDATE vacancies
            SET vacancy_close_date = ?
            WHERE id = ?
        ''', (close_date, vacancy_id))

        conn.commit()
        logger.info(f"Вакансия {vacancy_id} закрыта. Дата закрытия: {close_date}")
    except Exception as err:
        logger.error(f"Ошибка при закрытии вакансии {vacancy_id}: {err}")
        raise
    finally:
        conn.close()


def get_open_vacancies_links():
    """Возвращает список ID открытых вакансий"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM vacancies WHERE vacancy_close_date IS NULL OR vacancy_close_date = "False";')
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()


# Инициализация базы данных при первом импорте модуля
initialize_database()

if __name__ == "__main__":
    # Получаем и выводим информацию
    print(f"Общее количество вакансий: {get_total_vacancies()}")
