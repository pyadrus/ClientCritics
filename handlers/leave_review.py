# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.types import CallbackQuery

from dispatcher import router
from keyboards.keyboards import product_selection_keyboard
from messages.messages import table_model_prompt


@router.callback_query(F.data == "leave_review")
async def leave_review_handler(callback_query: CallbackQuery):
    """Пользователь выбрал 'Оставить отзыв'"""
    response_message = callback_query.message

    await response_message.edit_text(
        table_model_prompt,
        reply_markup=product_selection_keyboard()
    )


def register_leave_review_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(leave_review_handler)
