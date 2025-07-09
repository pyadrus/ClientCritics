# -*- coding: utf-8 -*-

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отвечает на команду /start
    """
    logger.info(f"Пользователь ввел команду /start: {message.from_user.full_name}")
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


def register_handlers() -> None:
    """Регистрация хендлера"""
    dp.message.register(command_start_handler)
