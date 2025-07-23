# -*- coding: utf-8 -*-
from aiogram.fsm.state import StatesGroup, State


class StatesNox(StatesGroup):
    """
    Состояния для бота для стола Nox.
    """
    size = State()  # Размер
    feedback = State()  # Отзыв
    photo_video = State()  # Фото и видео


class StatesPrimo(StatesGroup):
    """
    Состояния для бота для стола Primo.
    """
    size_primo = State()  # Размер
    colour_primo = State()  # Цвет
    feedback_primo = State()  # Отзыв
    photo_video_primo = State()  # Фото и видео
