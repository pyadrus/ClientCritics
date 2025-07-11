# -*- coding: utf-8 -*-

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards.keyboards import product_selection_keyboard


@router.callback_query(F.data == "leave_review")
async def leave_review_handler(callback_query: CallbackQuery, state: FSMContext):
    """Выбор продукта"""

    await bot.send_message(callback_query.from_user.id, "Выберите продукт", reply_markup=product_selection_keyboard())


def register_leave_review_handlers():
    """Регистрация обработчиков"""
    router.register_callback_query_handler(leave_review_handler)
