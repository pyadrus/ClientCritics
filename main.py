# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from dispatcher import bot, dp
from handlers.leave_review import register_leave_review_handlers
from handlers.nox import register_NOX_handlers
from handlers.primo import register_PRIMO_handlers
from handlers.review_moderation import register_handlers_publish
from handlers.start_menu import register_handlers


# https://docs.aiogram.dev/en/dev-3.x/

async def main() -> None:
    """
    Функция запуска бота
    :return:  None
    """
    await dp.start_polling(bot)
    register_handlers()

    register_leave_review_handlers()  # Выбор продукта для отзыва
    register_NOX_handlers()  # Отзывы NOX
    register_PRIMO_handlers()  # Отзывы PRIMO

    register_handlers_publish()  # Отправка отзывов на публикацию


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
