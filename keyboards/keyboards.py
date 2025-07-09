# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура старта"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить отзыв", callback_data="leave_review")],
        ]
    )
