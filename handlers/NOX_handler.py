# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards.NOX_keyboards import selection_size_arbo_primo_table_keyboard_nox, leave_review_nox_keyboard, \
    the_send_button_keyboard_nox


@router.callback_query(F.data == "the_nox_table")
async def the_nox_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите размер",
        reply_markup=selection_size_arbo_primo_table_keyboard_nox()
    )


@router.callback_query(F.data.in_({"solo_nox", "duo_nox", "atelier_nox", "grande_nox", "majestic_nox"}))
async def select_size_nox(callback_query: CallbackQuery, state: FSMContext):
    """Общий обработчик для выбора размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        "Оставить отзыв",
        reply_markup=leave_review_nox_keyboard()
    )


@router.callback_query(F.data == "leave_review_nox")
async def leave_review_nox(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Напишите отзыв и нажмите кнопку Отправить",
                           reply_markup=the_send_button_keyboard_nox())


@router.callback_query(F.data == "send_review_nox")
async def send_review_nox(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Ваш отзыв отправлен")


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.register_callback_query_handler(the_nox_table)  # Регистрация обработчика
    router.register_callback_query_handler(select_size_nox)  # Регистрация обработчика
    router.register_callback_query_handler(leave_review_nox)  # Регистрация обработчика
    router.register_callback_query_handler(send_review_nox)  # Регистрация обработчика
