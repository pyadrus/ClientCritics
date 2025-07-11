# -*- coding: utf-8 -*-

from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger
from dispatcher import dp
from keyboards.keyboards import start_keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отвечает на команду /start
    """
    logger.info(f"Пользователь ввел команду /start: {message.from_user.full_name}")
    text = (
        "Здравствуйте! Рад, что стол уже у Вас.\n\n"

        "Буду благодарен, если найдете немного о времени, и поделитесь своими впечатлениями.\n\n"

        "Не обязательно писать что-то официальное — просто расскажите, как Вам стол: ощущения, впечатления, детали, "
        "которые порадовали или удивили."
    )
    await message.answer(
        text=text,  # Текст сообщения пользователю
        reply_markup=start_keyboard()  # Клавиатура
    )


def register_handlers() -> None:
    """Регистрация хендлера"""
    dp.message.register(command_start_handler)
