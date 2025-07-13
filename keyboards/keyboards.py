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
            [InlineKeyboardButton(text="Стол ARBO PRIMO", callback_data="arbo_primo_table")],
            [InlineKeyboardButton(text="Стол NOX", callback_data="the_nox_table")],
        ]
    )

# # ========================
# # Выбор размера ARBO PRIMO, например  size = "solo" или "duo".  text = "Solo (120 × 75 см)" или "Duo (140 × 80 см)"
# # ========================
#
# TABLE_SIZES = {
#     "solo": "Solo (120 × 75 см)",
#     "duo": "Duo (140 × 80 см)",
#     "atelier": "Atelier (160 × 85 см)",
#     "grande": "Grande (180 × 90 см)",
#     "majestic": "Majestic (200 × 95 см)"
# }
#
#
# def selection_size_arbo_primo_table_keyboard() -> InlineKeyboardMarkup:
#     """
#     Возвращает клавиатуру для выбора размера стола ARBO PRIMO.
#     """
#     buttons = [
#         [InlineKeyboardButton(text=text, callback_data=size)]
#         for size, text in TABLE_SIZES.items()
#     ]
#
#     return InlineKeyboardMarkup(inline_keyboard=buttons)


# ========================
# Выбор цвета, например  color = "Молоко" или "Шёлк".  text = "Молоко" или "Шёлк"
# ========================

# COLOURS = [
#     "Молоко", "Шёлк", "Туман", "Лён", "Мох", "Солома", "Песчаник", "Миндаль", "Коньяк", "Янтарь",
#     "Орех карамельный", "Шоколад", "Мускат", "Уголь", "Эбен", "Терракот", "Медный", "Бесцветный"
# ]
#
#
# def selection_colour_keyboard() -> InlineKeyboardMarkup:
#     """
#     Возвращает клавиатуру для выбора цвета товара.
#     Разбивает цвета по строкам по 3 кнопки.
#     """
#     buttons = [InlineKeyboardButton(text=colour, callback_data=colour) for colour in COLOURS]
#
#     # Разбиваем список кнопок на строки по 3 элемента
#     keyboard_rows = [
#         buttons[i:i + 3]
#         for i in range(0, len(buttons), 3)
#     ]
#
#     return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
