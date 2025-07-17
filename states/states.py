# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    product = State()  # Продукт
    size = State()  # Размер
    colour = State()  # Цвет
    feedback = State()  # Отзыв
    sending = State()  # Отправка
    photo = State()  # Фото
    video = State()  # Видео
