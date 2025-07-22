# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




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
