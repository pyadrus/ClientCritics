import asyncio
import logging
import sys

from dispatcher import bot, dp


async def main() -> None:

    # запуск
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())