import asyncio
import logging
import sys

from dispatcher import bot, dp
from handlers.handlers import register_handlers

# https://docs.aiogram.dev/en/dev-3.x/

async def main() -> None:
    # запуск
    await dp.start_polling(bot)
    register_handlers()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
