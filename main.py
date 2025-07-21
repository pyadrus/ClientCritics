import asyncio
import logging
import sys

from loguru import logger

from dispatcher import bot, dp
from handlers.NOX_handler import register_NOX_handlers
from handlers.PRIMO_handler import register_PRIMO_handlers
from handlers.bot import register_handlers_publish
from handlers.handlers import register_handlers
from handlers.leave_review_handler import register_leave_review_handlers
from models.models import create_tables


# https://docs.aiogram.dev/en/dev-3.x/

async def main() -> None:
    create_tables()  # ✅ создание таблиц один раз при старте
    logger.info("🚀 Таблицы созданы или уже существуют")

    # запуск
    await dp.start_polling(bot)
    register_handlers()

    register_leave_review_handlers()  # Выбор продукта для отзыва
    register_NOX_handlers()  # Отзывы NOX
    register_PRIMO_handlers()  # Отзывы PRIMO

    register_handlers_publish()  # Отправка отзывов на публикацию


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
