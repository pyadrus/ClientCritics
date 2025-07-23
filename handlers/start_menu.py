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
from messages.messages import greeting_text

logger.add("log/log.log", enqueue=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Отвечает на команду /start
    """
    await state.clear()
    response_message = message
    logger.info(f"Пользователь ввел команду /start: {message.from_user.full_name}")
    await response_message.answer(
        text=greeting_text,  # Текст сообщения пользователю
        reply_markup=start_keyboard()  # Клавиатура
    )


@router.callback_query(F.data == "start_menu")
async def start_menu_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Отвечает на нажатие кнопки в меню 'Назад'"""
    await state.clear()
    response_message = callback.message
    logger.info(f"Пользователь вернулся в начальное меню: {callback.from_user.full_name}")
    await response_message.edit_text(
        greeting_text,
        reply_markup=start_keyboard()
    )


def register_handlers() -> None:
    """Регистрация хендлера"""
    dp.message.register(command_start_handler)
    router.callback_query.register(start_menu_callback_handler)
