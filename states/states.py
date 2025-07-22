# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    # product = State()  # Продукт
    size = State()  # Размер
    # colour = State()  # Цвет
    feedback = State()  # Отзыв

    sending = State()  # Отправка
    photo_video = State()  # Фото
    # video = State()  # Видео
    photo = State()  # Фото
    confirm = State()  # Подтверждение


class StatesPrimo(StatesGroup):
    # product = State()  # Продукт
    size_primo = State()  # Размер
    colour_primo = State()  # Цвет
    feedback_primo = State()  # Отзыв

    sending_primo = State()  # Отправка
    photo_video_primo = State()  # Фото
    # video = State()  # Видео
    photo_primo = State()  # Фото
    confirm_primo = State()  # Подтверждение
