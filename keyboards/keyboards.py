# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# ========================
# Стартовая клавиатура
# ========================

def start_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для начального экрана.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить отзыв", callback_data="leave_review")],
        ]
    )


# ========================
# Выбор продукта
# ========================

def product_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора типа стола.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Стол ARBO PRIMO", callback_data="arbo_primo_table"),
             InlineKeyboardButton(text="Стол ARBO NOX", callback_data="the_nox_table")],
            [InlineKeyboardButton(text="В начальное меню", callback_data="start_menu")],
        ]
    )
