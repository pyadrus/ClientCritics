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
            [InlineKeyboardButton(text="ARBO PRIMO", callback_data="arbo_primo_table"),
             InlineKeyboardButton(text="ARBO NOX", callback_data="nox_table")],
            [InlineKeyboardButton(text="В начальное меню", callback_data="start_menu")],
        ]
    )


# ========================
# Выбор размера ARBO PRIMO, например  size = "solo" или "duo".  text = "Solo (120 × 75 см)" или "Duo (140 × 80 см)"
# ========================

TABLE_SIZES_NOX = {
    "solo_nox": "Solo (120 × 75 см)",
    "duo_nox": "Duo (140 × 80 см)",
    "atelier_nox": "Atelier (160 × 85 см)",
    "grande_nox": "Grande (180 × 90 см)",
    "majestic_nox": "Majestic (200 × 95 см)",
}


def selection_size_table_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора размера стола ARBO PRIMO, NOX.
    """
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=size)]
        for size, text in TABLE_SIZES_NOX.items()
    ]
    # Добавляем кнопку "В начальное меню"
    buttons.append([
        InlineKeyboardButton(text="В начальное меню", callback_data="start_menu")
    ])
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
    # Добавляем кнопку "В начальное меню"
    # Добавляем кнопку "В начальное меню" как отдельную строку
    keyboard_rows.append([
        InlineKeyboardButton(text="В начальное меню", callback_data="start_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)


def keyboard_start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="В начальное меню", callback_data="start_menu"),
            ]])


def keyboard_confirm_or_cancel() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_review"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="start_menu")
        ]
    ])


def keyboard_confirm_or_cancel_primo() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_review_primo"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="start_menu")
        ]
    ])


def admin_keyboard():
    """
    Возвращает клавиатуру с двумя кнопками: "✅ Опубликовать" и "❌ Не публиковать", предназначенные для модерации
    контента администратором.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Опубликовать", callback_data="to_publish"),
             InlineKeyboardButton(text="❌ Не публиковать", callback_data="do_not_publish")],
        ]
    )
