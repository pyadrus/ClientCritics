# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
