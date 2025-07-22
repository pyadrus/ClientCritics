# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class StatesNox(StatesGroup):
    size = State()  # Размер
    feedback = State()  # Отзыв
    sending = State()  # Отправка
    photo_video = State()  # Фото
    # photo = State()  # Фото


class StatesPrimo(StatesGroup):
    size_primo = State()  # Размер
    colour_primo = State()  # Цвет
    feedback_primo = State()  # Отзыв
    sending_primo = State()  # Отправка
    photo_video_primo = State()  # Фото
    # photo_primo = State()  # Фото
    # confirm_primo = State()  # Подтверждение
