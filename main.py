import asyncio
import logging
import sys

from dispatcher import bot, dp
from handlers.handlers import register_handlers
from handlers.leave_review_handler import register_leave_review_handlers


# https://docs.aiogram.dev/en/dev-3.x/

async def main() -> None:
    # запуск
    await dp.start_polling(bot)
    register_handlers()

    register_leave_review_handlers()  # Выбор продукта для отзыва


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
