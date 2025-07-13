# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ========================
# Выбор размера ARBO PRIMO, например  size = "solo" или "duo".  text = "Solo (120 × 75 см)" или "Duo (140 × 80 см)"
# ========================

TABLE_SIZES_NOX = {
    "solo_nox": "Solo (120 × 75 см)",
    "duo_nox": "Duo (140 × 80 см)",
    "atelier_nox": "Atelier (160 × 85 см)",
    "grande_nox": "Grande (180 × 90 см)",
    "majestic_nox": "Majestic (200 × 95 см)"
}


def selection_size_arbo_primo_table_keyboard_nox() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора размера стола ARBO PRIMO.
    """
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=size)]
        for size, text in TABLE_SIZES_NOX.items()
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
