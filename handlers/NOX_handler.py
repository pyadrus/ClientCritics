# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from dispatcher import router, bot
from keyboards.NOX_keyboards import (selection_size_arbo_primo_table_keyboard_nox, leave_review_nox_keyboard,
                                     TABLE_SIZES_NOX)
from messages.messages import size_selection_text
from models.models import Review
from states.states import States


@router.callback_query(F.data == "the_nox_table")
async def the_nox_table(callback_query: CallbackQuery, state: FSMContext):
    """
    📌 Обработчик нажатия на кнопку "ARBO PRIMO".
    Показывает пользователю клавиатуру выбора размера стола.
    """
    await bot.send_message(
        callback_query.from_user.id,
        size_selection_text,
        reply_markup=selection_size_arbo_primo_table_keyboard_nox()
    )
    await state.set_state(States.size)


@router.callback_query(StateFilter(States.size), F.data.in_(TABLE_SIZES_NOX.keys()))
async def select_size_nox(callback_query: CallbackQuery, state: FSMContext):
    """
    📌 Обработка выбранного размера стола.
    Сохраняет его в состояние FSM и предлагает оставить отзыв.
    """
    selected_size = callback_query.data
    readable = TABLE_SIZES_NOX[selected_size]  # selected_size — это ключ
    await state.update_data(size=selected_size)

    logger.info(f"🟢 [{callback_query.from_user.id}] Выбран размер: {readable}")

    await bot.send_message(
        callback_query.from_user.id,
        "✍️ Хотите оставить отзыв?",
        reply_markup=leave_review_nox_keyboard()
    )
    await state.set_state(States.feedback)


@router.callback_query(StateFilter(States.feedback), F.data == "leave_review_nox")
async def leave_review_nox(callback_query: CallbackQuery, state: FSMContext):
    """
    ✍️ Пользователь нажал "Оставить отзыв".
    Переходим в состояние ожидания текстового отзыва.
    """
    await state.update_data(feedback="yes")

    logger.info(f"🟡 [{callback_query.from_user.id}] Пользователь согласился оставить отзыв")

    await bot.send_message(
        callback_query.from_user.id,
        "📝 Напишите ваш отзыв в сообщении 👇"
    )
    await state.set_state(States.sending)


@router.message(StateFilter(States.sending))
async def send_review_nox(message: Message, state: FSMContext):
    """
    Обработка нажатия на кнопку "Отправить".
    Сохраняет все данные в базу и завершает процесс.
    """
    data = await state.get_data()
    user_id = message.from_user.id
    table_size = data.get("size", "unknown")
    readable = TABLE_SIZES_NOX[table_size]  # selected_size — это ключ
    feedback_status = data.get("feedback", "no")
    feedback_text = message.text.strip()
    # Сохраняем в базу данных
    Review.create(
        user_id=user_id,
        table_size=readable,
        feedback_status=feedback_status,
        feedback_text=feedback_text
    )

    logger.success(f"✅ [{user_id}] Отзыв сохранён: size={readable}, text={feedback_text}")

    await message.answer("🎉 Спасибо за ваш отзыв! Он был успешно сохранён 🙌")
    await state.clear()


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(the_nox_table)  # Регистрация обработчика
    router.callback_query.register(select_size_nox)  # Регистрация обработчика
    router.callback_query.register(leave_review_nox)  # Регистрация обработчика
    router.callback_query.register(send_review_nox)  # Регистрация обработчика
