# -*- coding: utf-8 -*-

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message

from dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отвечает на команду /start
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
