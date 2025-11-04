import os
from dotenv import load_dotenv
from telegram import Bot
import datetime
import pytz
import asyncio
from src.utils.main_logger import setup_logger

# Инициализация логера для текущего модуля
logger = setup_logger(__name__)

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен и ID чата из переменных окружения
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

async def send_simple_message(text: str = "Пустое сообщение", max_retries: int = 3):
    """
    Асинхронная функция для отправки сообщения в Telegram с повторными попытками.
    """
    # Проверяем, что переменные загружены
    if not bot_token or not chat_id:
        logger.error("Ошибка: Токен бота или ID чата не найдены в .env файле.")
        return

    # Создаём экземпляр бота
    bot = Bot(token=bot_token)
    utc_now = datetime.datetime.now(datetime.UTC)
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_now = utc_now.astimezone(moscow_tz)
    formatted_time = moscow_now.strftime('%d.%m.%Y, %H:%M')
    date = formatted_time

    # Сообщение, которое мы хотим отправить
    message_text = f'🟢 hh_ru Parser:\n\n📅 Дата и время отправки: {date}\n\n📊 Данные:\n{text}'

    for attempt in range(max_retries):
        try:
            # Отправляем сообщение
            await bot.send_message(chat_id=chat_id, text=message_text)
            logger.info("Сообщение успешно отправлено!")
            return
        except Exception as e:
            logger.warning(f"Попытка {attempt + 1} из {max_retries} не удалась: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(2)  # Ждем 2 секунды перед следующей попыткой
            else:
                logger.error(f"Не удалось отправить сообщение после {max_retries} попыток: {e}")

if __name__ == '__main__':
    # Запускаем асинхронную функцию
    asyncio.run(send_simple_message("test bot"))
