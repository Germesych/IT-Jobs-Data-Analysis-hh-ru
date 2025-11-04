from src.check_vacancy_status.vacancy_checker import check_vacancy_status
from src.crawl_links.link_crawler import crawl_links
from src.database.db_manager import get_total_vacancies, get_today_vacancies_count
from src.parser.vacancy_parser import parser
from src.utils.telegram_bot import send_simple_message
import psutil
import time

try:
    process = psutil.Process()
    start_time = time.time()
    start_cpu = process.cpu_percent(interval=None)
    start_memory = process.memory_info().rss
except Exception as err:
    print(err)


def main():
    parser()
    crawl_links(False, "16_vacancies_links.txt")
    crawl_links(False, "113_vacancies_links.txt")
    # get_total_vacancies()
    # get_today_vacancies_count()
    # get_last_vacancy()


if __name__ == "__main__":
    import asyncio

    main()  # модуотный код
    # check_vacancy_status() # просто функуия
    # main() # модуотный код

    end_cpu = process.cpu_percent(interval=None)
    end_memory = process.memory_info().rss
    end_time = time.time()
    execution_time = end_time - start_time

    # Преобразование секунд в часы, минуты и секунды
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = int(execution_time % 60)

    usage_CPU = f"CPU: {end_cpu}%"
    usage_Memory = f"Memory: {end_memory / (1024 * 1024)} MB"
    usage_time = f"Время выполнения: {hours:02d}:{minutes:02d}:{seconds:02d}"
    vacancies_info = f"Все вакансии в базе: {get_total_vacancies()}\nСегодня добавлено: {get_today_vacancies_count()}"

    print(f"{usage_CPU}\n{usage_Memory}\n{usage_time}")
    print(
        f"Все вакансии в базе: {get_total_vacancies()}\nСегодня добавлено: {get_today_vacancies_count()}"
    )

    message = f"(Mac)\n{usage_CPU}\n{usage_Memory}\n{usage_time}\n{vacancies_info}"
    asyncio.run(send_simple_message(message))
