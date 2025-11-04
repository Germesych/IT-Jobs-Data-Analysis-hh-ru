import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Определяем режим работы (dev/prod)
APP_ENV = os.getenv('APP_ENV', 'dev')

def setup_logger(name):
    """Настройка логгера с учетом режима работы."""
    logger = logging.getLogger(name)
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.WARNING)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Обработчики в зависимости от режима
    if APP_ENV == 'production':
        logger.setLevel(logging.INFO)
        # Логи в файл с ротацией (максимум 5 файлов по 10 МБ)
        file_handler = RotatingFileHandler(
            'app.log',
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # Логи в консоль в режиме разработки
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

"""
from src.utils.main_logger import setup_logger
logger = setup_logger(__name__)

def get_vacancies_metadata(role: int = 96, area: int = 113, page: int = 0) -> dict:
    # ... ваш код ...
    logger.info(f"get_vacancies_metadata: {data}")
    return data
"""
