## 🗺️ Карта JSON одной вакансии (структура и описание полей)

```json
{
  "id": "124021845",
  "premium": false,
  "name": "Программист-стажер 1С",
  "department": null,
  "has_test": false,
  "response_letter_required": false,
  "area": {
    "id": "41",
    "name": "Калининград",
    "url": "https://api.hh.ru/areas/41"
  },
  "salary": {
    "from": 45000,
    "to": 90000,
    "currency": "RUR",
    "gross": false
  },
  "salary_range": { ... },  // дублирует salary, но с дополнительной мета-информацией
  "type": {
    "id": "open",
    "name": "Открытая"
  },
  "address": {
    "city": "Калининград",
    "street": "Ленинский проспект",
    "building": "131",
    "lat": 54.698697,
    "lng": 20.503436,
    "description": null,
    "raw": "Калининград, Ленинский проспект, 131",
    "metro": null,
    "metro_stations": [],
    "id": "7324198"
  },
  "response_url": null,
  "sort_point_distance": null,
  "published_at": "2025-08-19T16:24:09+0300",
  "created_at": "2025-08-19T16:24:09+0300",
  "archived": false,
  "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=124021845",
  "show_logo_in_search": null,
  "show_contacts": true,
  "insider_interview": null,
  "url": "https://api.hh.ru/vacancies/124021845?host=hh.ru",
  "alternate_url": "https://hh.ru/vacancy/124021845",
  "relations": [],
  "employer": { ... },  // данные компании
  "snippet": { ... },   // краткое описание требований и обязанностей
  "contacts": null,
  "schedule": {
    "id": "fullDay",
    "name": "Полный день"
  },
  "working_days": [],
  "working_time_intervals": [],
  "working_time_modes": [],
  "accept_temporary": false,
  "fly_in_fly_out_duration": [],
  "work_format": [],
  "working_hours": [
    { "id": "OTHER", "name": "Другое" }
  ],
  "work_schedule_by_days": [
    { "id": "OTHER", "name": "Другое" }
  ],
  "night_shifts": false,
  "professional_roles": [
    { "id": "96", "name": "Программист, разработчик" }
  ],
  "accept_incomplete_resumes": true,
  "experience": {
    "id": "noExperience",
    "name": "Нет опыта"
  },
  "employment": {
    "id": "full",
    "name": "Полная занятость"
  },
  "employment_form": {
    "id": "FULL",
    "name": "Полная"
  },
  "internship": false,
  "adv_response_url": null,
  "is_adv_vacancy": false,
  "adv_context": null
}
```

---

## 📚 Полный список полей и их описание

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | string | Уникальный идентификатор вакансии |
| `premium` | boolean | Является ли вакансия платной (рекламной) |
| `name` | string | Название вакансии |
| `department` | object/null | Подразделение в компании (если указано) |
| `has_test` | boolean | Есть ли тестовое задание |
| `response_letter_required` | boolean | Требуется ли сопроводительное письмо |
| `area` | object | Регион/город размещения вакансии |
| `area.id` | string | ID региона (из справочника areas) |
| `area.name` | string | Название региона (например, Москва) |
| `area.url` | string | Ссылка на API региона |
| `salary` | object/null | Информация о зарплате |
| `salary.from` | number/null | Минимальная зарплата |
| `salary.to` | number/null | Максимальная зарплата |
| `salary.currency` | string | Валюта (RUR, USD, EUR и т.д.) |
| `salary.gross` | boolean | `true` — до вычета налогов, `false` — на руки |
| `salary_range` | object/null | Расширенная информация о зарплате (аналогично `salary`, но с mode/frequency) |
| `type` | object | Тип вакансии |
| `type.id` | string | `open`, `closed`, `hidden` и др. |
| `type.name` | string | Человекочитаемое название типа |
| `address` | object/null | Адрес офиса |
| `address.city` | string | Город |
| `address.street` | string | Улица |
| `address.building` | string | Номер здания |
| `address.lat`, `lng` | number | Координаты |
| `address.raw` | string | Полный адрес одной строкой |
| `address.metro` | object/null | Ближайшее метро (если есть) |
| `address.metro_stations` | array | Список ближайших станций метро |
| `address.id` | string | ID адреса в системе |
| `response_url` | string/null | Ссылка для отклика (если внешняя) |
| `sort_point_distance` | number/null | Расстояние до точки сортировки (для поиска рядом) |
| `published_at` | string (ISO 8601) | Дата публикации вакансии |
| `created_at` | string (ISO 8601) | Дата создания вакансии |
| `archived` | boolean | Архивирована ли вакансия |
| `apply_alternate_url` | string | Ссылка для отклика через HH |
| `show_logo_in_search` | boolean/null | Показывать ли логотип в поиске |
| `show_contacts` | boolean | Показывать ли контакты работодателя |
| `insider_interview` | object/null | Информация о "Insider Interview" (редко) |
| `url` | string | Ссылка на API вакансии |
| `alternate_url` | string | Ссылка на страницу вакансии на сайте HH |
| `relations` | array | Связанные объекты (например, приглашения) |
| `employer` | object | Информация о работодателе |
| `employer.id` | string | ID компании |
| `employer.name` | string | Название компании |
| `employer.url` | string | Ссылка на API компании |
| `employer.alternate_url` | string | Ссылка на страницу компании |
| `employer.logo_urls` | object/null | Ссылки на логотипы разного размера |
| `employer.vacancies_url` | string | Ссылка на вакансии компании |
| `employer.accredited_it_employer` | boolean | Аккредитованный IT-работодатель |
| `employer.trusted` | boolean | Проверенный работодатель |
| `snippet` | object | Краткое описание из вакансии |
| `snippet.requirement` | string/null | Требования к кандидату |
| `snippet.responsibility` | string/null | Обязанности |
| `contacts` | object/null | Контактное лицо (имя, телефон, email) — редко |
| `schedule` | object | График работы |
| `schedule.id` | string | `fullDay`, `remote`, `flexible`, `shift`, `flyInFlyOut` |
| `schedule.name` | string | "Полный день", "Удалённая работа" и т.д. |
| `working_days` | array | Дни работы (например, `["mon", "tue"]`) — редко используется |
| `working_time_intervals` | array | Интервалы рабочего времени — редко |
| `working_time_modes` | array | Режимы времени (например, "сменный") |
| `accept_temporary` | boolean | Принимаются временные работники |
| `fly_in_fly_out_duration` | array | Длительность вахты (если `flyInFlyOut`) |
| `work_format` | array | Формат работы: `ON_SITE`, `REMOTE`, `HYBRID` |
| `working_hours` | array | Продолжительность рабочего дня: `HOURS_8`, `HOURS_9`, `OTHER` |
| `work_schedule_by_days` | array | Расписание по дням: `FIVE_ON_TWO_OFF`, `OTHER` |
| `night_shifts` | boolean | Есть ли ночные смены |
| `professional_roles` | array | Профессиональные роли (например, "Программист") |
| `professional_roles[0].id` | string | ID роли |
| `professional_roles[0].name` | string | Название роли |
| `accept_incomplete_resumes` | boolean | Можно ли откликаться с незавершённым резюме |
| `experience` | object | Опыт работы |
| `experience.id` | string | `noExperience`, `between1And3`, `between3And6`, `moreThan6` |
| `experience.name` | string | "Нет опыта", "От 1 года до 3 лет" и т.д. |
| `employment` | object | Тип занятости |
| `employment.id` | string | `full`, `part`, `project`, `volunteer`, `probation` |
| `employment.name` | string | "Полная занятость", "Частичная" и т.д. |
| `employment_form` | object | Форма занятости |
| `employment_form.id` | string | `FULL`, `PART`, `PROJECT`, `VOLUNTEER` |
| `employment_form.name` | string | "Полная", "Проектная" и т.д. |
| `internship` | boolean | Является ли стажировкой |
| `adv_response_url` | string/null | Рекламная ссылка для отклика |
| `is_adv_vacancy` | boolean | Является ли рекламной вакансией |
| `adv_context` | object/null | Контекст рекламы (если есть) |

---

## 🔍 Что полезно извлекать при парсинге

Если ты парсишь вакансии, чаще всего интересуют:

```python
{
    "id": vacancy["id"],
    "title": vacancy["name"],
    "company": vacancy["employer"]["name"],
    "city": vacancy["area"]["name"],
    "salary_from": vacancy.get("salary", {}).get("from"),
    "salary_to": vacancy.get("salary", {}).get("to"),
    "currency": vacancy.get("salary", {}).get("currency"),
    "gross": vacancy.get("salary", {}).get("gross"),
    "experience": vacancy["experience"]["name"],
    "employment": vacancy["employment"]["name"],
    "schedule": vacancy["schedule"]["name"],
    "work_format": [wf["name"] for wf in vacancy.get("work_format", [])],
    "requirements": vacancy["snippet"].get("requirement"),
    "responsibilities": vacancy["snippet"].get("responsibility"),
    "published_at": vacancy["published_at"],
    "url": vacancy["alternate_url"].strip()
}
```

---

## 💡 Советы

- Используй `.get("key", default)` чтобы избежать `KeyError`.
- Обрезай строки: `.strip()` у `url`, `name` и т.д.
- Зарплата может быть `null` — проверяй.
- `snippet` может быть пустым — используй `.get()`.

