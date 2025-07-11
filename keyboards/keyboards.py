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
            [InlineKeyboardButton(text="Стол ARBO PRIMO", callback_data="arbo_primo_table")],
            [InlineKeyboardButton(text="Стол ARBO", callback_data="arbo_table")],
            [InlineKeyboardButton(text="Стол NOX", callback_data="the_nox_table")],
        ]
    )


def selection_size_arbo_primo_table_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора товара"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Solo (120 × 75 см)", callback_data="solo")],
            [InlineKeyboardButton(text="Duo (140 × 80 см)", callback_data="duo")],
            [InlineKeyboardButton(text="Atelier (160 × 85 см)", callback_data="atelier")],
            [InlineKeyboardButton(text="Grande (180 × 90 см)", callback_data="grande")],
            [InlineKeyboardButton(text="Majestic (200 × 95 см)", callback_data="majestic")],
        ]
    )
