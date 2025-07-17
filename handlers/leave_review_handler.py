# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router
from keyboards.keyboards import product_selection_keyboard


@router.callback_query(F.data == "leave_review")
async def leave_review_handler(callback_query: CallbackQuery, state: FSMContext):
    """Пользователь выбрал 'Оставить отзыв'"""
    response_message = callback_query.message

    await response_message.edit_text(
        "Выберите продукт",
        reply_markup=product_selection_keyboard()
    )


def register_leave_review_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(leave_review_handler)
