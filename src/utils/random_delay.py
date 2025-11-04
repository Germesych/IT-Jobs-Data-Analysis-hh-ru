import random
import time
from src.utils.main_logger import setup_logger
logger = setup_logger(__name__)

def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """Приостанавливает выполнение на случайное время в заданном диапазоне.

    Args:
        min_seconds (float): Минимальная задержка в секундах (по умолчанию: 1.0).
        max_seconds (float): Максимальная задержка в секундах (по умолчанию: 3.0).

    Returns:
        None

    Example:
        >>> random_delay(min_seconds=0.5, max_seconds=2.0)  # Задержка от 0.5 до 2 секунд
    """
    delay = random.uniform(min_seconds, max_seconds)
    logger.debug(f"Задержка на {delay:.2f} секунд...")
    time.sleep(delay)
