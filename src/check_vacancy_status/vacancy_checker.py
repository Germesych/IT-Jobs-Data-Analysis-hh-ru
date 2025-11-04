from src.crawl_links.main_requests import fetch_vacancy_data
from datetime import datetime
from src.database.db_manager import get_open_vacancies_links, close_vacancy


def check_vacancy_status():
    list_vacancies_ids = get_open_vacancies_links()
    closed_positions = 0
    all_vacancies_processed = 0
    country = 0

    for vacancy_id in list_vacancies_ids:
        link = f"https://api.hh.ru/vacancies/{vacancy_id}?host=hh.ru"
        data = fetch_vacancy_data(link)
        country +=1
        print(f"it work... {country} in {len(list_vacancies_ids)}")

        # Проверяем, что данные получены и валидны
        if data is None:
            print(f"Не удалось получить данные для вакансии {vacancy_id}")
            continue

        if not isinstance(data, dict):
            print(f"Некорректный формат данных для вакансии {vacancy_id}")
            continue

        if data.get('closed'):
            vacancy_closed = datetime.now().isoformat(),
            closed_positions +=1
            try:
                close_vacancy(vacancy_id)
                print(f"link_crawler_vacancy_close: \n'vacancy_id':{vacancy_id}, \n'vacancy_closed': {vacancy_closed}\n----------\n")
            except Exception as err:
                print(f'Проблемы обновления данных о закрытой вакансии {vacancy_id} \nError:{err}')
        # else:
        #     print(f"вакансия еще не закрыта {vacancy_id}!")
        all_vacancies_processed += 1

    # print(f"Проверка закрытых вакансий отработала успешно!")
    # print(f"Закрылось вакансий: {closed_positions}")
    # print(f"Всех вакансйи обработано: {all_vacancies_processed}")

if __name__ == "__main__":
    check_vacancy_status()