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


# ========================
# Выбор размера ARBO PRIMO, например  size = "solo" или "duo".  text = "Solo (120 × 75 см)" или "Duo (140 × 80 см)"
# ========================

TABLE_SIZES = {
    "solo_primo": "Solo (120 × 75 см)",
    "duo_primo": "Duo (140 × 80 см)",
    "atelier_primo": "Atelier (160 × 85 см)",
    "grande_primo": "Grande (180 × 90 см)",
    "majestic_primo": "Majestic (200 × 95 см)"
}


def selection_size_arbo_primo_table_keyboard_primo() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора размера стола ARBO PRIMO.
    """
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=size)]
        for size, text in TABLE_SIZES.items()
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ========================
# Выбор цвета, например  color = "Молоко" или "Шёлк".  text = "Молоко" или "Шёлк"
# ========================
COLOURS = {
    "milk": "Молоко",
    "silk": "Шёлк",
    "fog": "Туман",
    "flax": "Лён",
    "moss": "Мох",
    "straw": "Солома",
    "sandstone": "Песчаник",
    "almond": "Миндаль",
    "brandy": "Коньяк",
    "amber": "Янтарь",
    "caramel_nut": "Орех карамельный",
    "chocolate": "Шоколад",
    "nutmeg": "Мускат",
    "coal": "Уголь",
    "ebony": "Эбен",
    "terracotta": "Терракот",
    "copper": "Медный",
    "colorless": "Бесцветный"
}


def selection_colour_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора цвета товара.
    Разбивает цвета по строкам по 3 кнопки.
    Текст кнопки — русское название цвета, callback_data — английский ключ.
    """
    buttons = [
        InlineKeyboardButton(text=ru_name, callback_data=en_key)
        for en_key, ru_name in COLOURS.items()
    ]

    # Разбиваем список кнопок на строки по 3 элемента
    keyboard_rows = [
        buttons[i:i + 3]
        for i in range(0, len(buttons), 3)
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)


def leave_review_primo_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура согласия отставить отзыв"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить отзыв", callback_data="leave_review_primo")],
        ]
    )


def the_send_button_keyboard_primo() -> InlineKeyboardMarkup:
    """Клавиатура согласия отправить отзыв"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Отправить", callback_data="send_review_primo"),
            ]
        ]
    )
