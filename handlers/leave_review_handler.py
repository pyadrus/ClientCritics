# -*- coding: utf-8 -*-

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards.keyboards import product_selection_keyboard, selection_size_arbo_primo_table_keyboard


@router.callback_query(F.data == "leave_review")
async def leave_review_handler(callback_query: CallbackQuery, state: FSMContext):
    """Выбор продукта"""
    await bot.send_message(callback_query.from_user.id, "Выберите продукт", reply_markup=product_selection_keyboard())


@router.callback_query(F.data == "arbo_primo_table")
async def arbo_primo_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите размер",
                           reply_markup=selection_size_arbo_primo_table_keyboard())


"""Выбор размера arbo_primo_table"""


@router.callback_query(F.data == "solo")
async def solo(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет",
                           reply_markup=selection_size_arbo_primo_table_keyboard())


@router.callback_query(F.data == "duo")
async def duo(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет",
                           reply_markup=selection_size_arbo_primo_table_keyboard())


@router.callback_query(F.data == "atelier")
async def atelier(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет",
                           reply_markup=selection_size_arbo_primo_table_keyboard())


@router.callback_query(F.data == "grande")
async def grande(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет",
                           reply_markup=selection_size_arbo_primo_table_keyboard())


@router.callback_query(F.data == "majestic")
async def majestic(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет",
                           reply_markup=selection_size_arbo_primo_table_keyboard())


@router.callback_query(F.data == "arbo_table")
async def arbo_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет", )


@router.callback_query(F.data == "the_nox_table")
async def the_nox_table(callback_query: CallbackQuery, state: FSMContext):
    """Выбор цвета"""
    await bot.send_message(callback_query.from_user.id, "Выберите цвет", )


def register_leave_review_handlers():
    """Регистрация обработчиков"""
    router.register_callback_query_handler(leave_review_handler)
    router.register_callback_query_handler(arbo_primo_table)
    router.register_callback_query_handler(arbo_table)
    router.register_callback_query_handler(the_nox_table)

    # Выбор размера
    router.register_callback_query_handler(solo)
    router.register_callback_query_handler(duo)
    router.register_callback_query_handler(atelier)
    router.register_callback_query_handler(grande)
    router.register_callback_query_handler(majestic)
