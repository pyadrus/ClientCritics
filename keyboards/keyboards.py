# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура старта"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить отзыв", callback_data="leave_review")],
        ]
    )


def product_selection_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора товара"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Стол BLACK EDGE", callback_data="black_edge_table")],
            [InlineKeyboardButton(text="Стол NORD", callback_data="the_nord_table")],
        ]
    )
