# -*- coding: utf-8 -*-

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards.keyboards import (
    product_selection_keyboard,
    selection_size_arbo_primo_table_keyboard,
    selection_colour_keyboard
)


@router.callback_query(F.data == "leave_review")
async def leave_review_handler(callback_query: CallbackQuery, state: FSMContext):
    """Пользователь выбрал 'Оставить отзыв'"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите продукт",
        reply_markup=product_selection_keyboard()
    )


@router.callback_query(F.data == "arbo_primo_table")
async def arbo_primo_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите размер",
        reply_markup=selection_size_arbo_primo_table_keyboard()
    )


"""Выбор размера arbo_primo_table"""


@router.callback_query(F.data.in_({"solo", "duo", "atelier", "grande", "majestic"}))
async def select_size(callback_query: CallbackQuery, state: FSMContext):
    """Общий обработчик для выбора размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите цвет",
        reply_markup=selection_colour_keyboard()
    )


"""Выбор цвета"""


@router.callback_query(F.data.in_({"arbo_table", "the_nox_table"}))
async def select_colour(callback_query: CallbackQuery, state: FSMContext):
    """Общий обработчик для выбора цвета других столов"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите цвет",
        reply_markup=selection_colour_keyboard()
    )


def register_leave_review_handlers():
    """Регистрация обработчиков"""
    router.register_callback_query_handler(leave_review_handler)
    router.register_callback_query_handler(arbo_primo_table)
    router.register_callback_query_handler(select_colour)

    # Выбор размера
    router.register_callback_query_handler(select_size)
