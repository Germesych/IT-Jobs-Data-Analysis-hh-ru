from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class VacancyData:
    id: int
    title: str
    url: str
    api_url: str
    published_at: datetime
    salary_from: int | None
    salary_to: int | None
    currency: str | None
    city: str
    country_code: str
    address: str | None
    employer_name: str
    employer_url: str
    employer_site: str | None
    key_skills: List[str]
    description: str
    experience: str | None = None
    is_archived: bool = False
