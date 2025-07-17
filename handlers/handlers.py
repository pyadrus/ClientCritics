# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from loguru import logger

from dispatcher import dp
from dispatcher import router
from keyboards.keyboards import start_keyboard

logger.add("log/log.log", enqueue=True)

text = (
    "Здравствуйте! Рад, что стол уже у Вас.\n\n"

    "Буду благодарен, если найдете немного о времени, и поделитесь своими впечатлениями.\n\n"

    "Не обязательно писать что-то официальное — просто расскажите, как Вам стол: ощущения, впечатления, детали, "
    "которые порадовали или удивили."
)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отвечает на команду /start
    """
    response_message = message
    logger.info(f"Пользователь ввел команду /start: {message.from_user.full_name}")

    await response_message.answer(
        text=text,  # Текст сообщения пользователю
        reply_markup=start_keyboard()  # Клавиатура
    )


@router.callback_query(F.data == "start_menu")
async def start_menu_callback_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Отвечает на нажатие кнопки в меню 'Назад'"""
    response_message = callback_query.message
    logger.info(f"Пользователь вернулся в начальное меню: {callback_query.from_user.full_name}")

    await response_message.edit_text(
        text,
        reply_markup=start_keyboard()
    )


def register_handlers() -> None:
    """Регистрация хендлера"""
    dp.message.register(command_start_handler)
    router.callback_query.register(start_menu_callback_handler)
