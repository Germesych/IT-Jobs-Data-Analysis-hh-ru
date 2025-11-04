"""Модуль с параметрами поиска вакансий."""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class VacancySearchParams:
    """Параметры поиска вакансий.

    Attributes:
        professional_role (int): ID профессиональной роли (по умолчанию: 96 — IT).
        area (int): ID региона поиска (по умолчанию: 113 — Россия).
        per_page (int): Количество вакансий на странице (по умолчанию: 100).
        page (int): Номер страницы (по умолчанию: 0).
        date_from (str): Дата начала поиска в формате 'YYYY-MM-DD' (по умолчанию: текущая дата).
        date_to (str): Дата окончания поиска в формате 'YYYY-MM-DD' (по умолчанию: текущая дата).
    """
    professional_role: int = 96
    area: int = 113
    per_page: int = 100
    page: int = 0
    date_from: str = datetime.now().strftime('%Y-%m-%d')
    date_to: str = datetime.now().strftime('%Y-%m-%d')
