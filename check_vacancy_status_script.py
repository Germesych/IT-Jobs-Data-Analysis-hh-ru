import asyncio
import psutil
import os
import time
import logging
from datetime import timedelta
from src.check_vacancy_status.vacancy_checker import check_vacancy_status
from src.database.db_manager import get_total_vacancies, get_today_vacancies_count
from src.utils.telegram_bot import send_simple_message

logging.basicConfig(level=logging.INFO)


async def main():
    try:
        process = psutil.Process(os.getpid())
        start_time = time.time()
        start_cpu = process.cpu_percent(interval=0.1)
        start_memory = process.memory_info().rss

        await send_simple_message("(Mac) Проверка статуса вакансий запущена!")
        check_vacancy_status()

        end_cpu = process.cpu_percent(interval=0.1)
        end_memory = process.memory_info().rss
        end_time = time.time()
        execution_time = end_time - start_time

        hours, remainder = divmod(execution_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        usage_time = (
            f"Время выполнения: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        )
        usage_CPU = f"CPU: {end_cpu}%"
        usage_Memory = f"Memory: {end_memory / (1024 * 1024):.2f} MB"

        total_vacancies = get_total_vacancies()
        today_vacancies = get_today_vacancies_count()
        vacancies_info = f"Все вакансии в базе: {total_vacancies}\nСегодня добавлено: {today_vacancies}"

        message = f"(Mac)Проверка статуса вакансий:\n{usage_CPU}\n{usage_Memory}\n{usage_time}\n{vacancies_info}"
        await send_simple_message(message)

    except Exception as err:
        logging.error(f"Ошибка: {err}")


if __name__ == "__main__":
    asyncio.run(main())
