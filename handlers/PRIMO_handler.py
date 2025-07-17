# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards.PRIMO_keyboards import (selection_size_arbo_primo_table_keyboard_primo, selection_colour_keyboard,
                                       leave_review_primo_keyboard, the_send_button_keyboard_primo)
from messages.messages import size_selection_text


@router.callback_query(F.data == "arbo_primo_table")
async def arbo_primo_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        size_selection_text,
        reply_markup=selection_size_arbo_primo_table_keyboard_primo()
    )


@router.callback_query(F.data.in_({"solo_primo", "duo_primo", "atelier_primo", "grande_primo", "majestic_primo"}))
async def select_size(callback_query: CallbackQuery, state: FSMContext):
    """Общий обработчик для выбора размера стола ARBO PRIMO"""
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите цвет Primo",
        reply_markup=selection_colour_keyboard()
    )


@router.callback_query(F.data.in_(
    {"milk", "silk", "fog", "flax", "moss", "straw", "sandstone", "almond", "brandy", "amber", "caramel_nut",
     "chocolate", "nutmeg", "coal", "ebony", "terracotta", "copper", "colorless"}))
async def select_colour_primo(callback_query: CallbackQuery, state: FSMContext):
    await bot.send_message(
        callback_query.from_user.id,
        "Оставьте отзыв",
        reply_markup=leave_review_primo_keyboard()
    )


@router.callback_query(F.data == "leave_review_primo")
async def leave_review_primo(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Напишите отзыв и нажмите кнопку Отправить",
                           reply_markup=the_send_button_keyboard_primo())


@router.callback_query(F.data == "send_review_primo")
async def send_review_primo(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Ваш отзыв отправлен")


def register_PRIMO_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(arbo_primo_table)
    router.callback_query.register(select_size)
    router.callback_query.register(select_colour_primo)

    router.callback_query.register(leave_review_primo)
    router.callback_query.register(send_review_primo)
