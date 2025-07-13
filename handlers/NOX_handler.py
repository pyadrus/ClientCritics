# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards.NOX_keyboards import selection_size_arbo_primo_table_keyboard_nox


@router.callback_query(F.data == "the_nox_table")
async def the_nox_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите размер",
        reply_markup=selection_size_arbo_primo_table_keyboard_nox()
    )


# @router.callback_query(F.data.in_({"solo", "duo", "atelier", "grande", "majestic"}))
# async def select_size(callback_query: CallbackQuery, state: FSMContext):
#     """Общий обработчик для выбора размера стола ARBO PRIMO"""
#     await bot.send_message(
#         callback_query.from_user.id,
#         "Выберите цвет",
#         reply_markup=selection_colour_keyboard()
#     )

#
# """Выбор цвета"""


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.register_callback_query_handler(the_nox_table)
