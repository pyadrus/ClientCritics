# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from dispatcher import router, bot
from keyboards.NOX_keyboards import (selection_size_arbo_primo_table_keyboard_nox, TABLE_SIZES_NOX, keyboard_start_menu,
                                     keyboard_video_handler)
from messages.messages import size_selection_text
from models.models import Review
from states.states import States

ADMIN_ID = 535185511  # ID администратора


@router.callback_query(F.data == "the_nox_table")
async def the_nox_table(callback_query: CallbackQuery, state: FSMContext):
    """
    📌 Обработчик нажатия на кнопку "ARBO PRIMO".
    Показывает пользователю клавиатуру выбора размера стола.
    """
    response_message = callback_query.message
    await response_message.edit_text(
        size_selection_text,
        reply_markup=selection_size_arbo_primo_table_keyboard_nox()
    )
    await state.set_state(States.size)


@router.callback_query(StateFilter(States.size), F.data.in_(TABLE_SIZES_NOX.keys()))
async def select_size_nox(callback_query: CallbackQuery, state: FSMContext):
    """
    ✍️ Пользователь нажал "Оставить отзыв".
    Переходим в состояние ожидания текстового отзыва.
    """
    response_message = callback_query.message
    selected_size = callback_query.data
    readable = TABLE_SIZES_NOX[selected_size]  # selected_size — это ключ
    await state.update_data(size=selected_size)
    logger.info(f"🟢 [{callback_query.from_user.id}] Выбран размер: {readable}")
    # logger.info(f"🟡 [{callback_query.from_user.id}] Пользователь согласился оставить отзыв")

    await response_message.edit_text(
        "📝 Напишите ваш отзыв в сообщении 👇", reply_markup=keyboard_start_menu()
    )
    await state.set_state(States.photo)


@router.message(StateFilter(States.photo))
async def send_photo_handler(message: Message, state: FSMContext):
    """
    Сохраняет отзыв и просит пользователя отправить фото.
    """
    # Сохраняем текст отзыва
    feedback_text = message.text.strip()
    await state.update_data(feedback=feedback_text)

    # Удаляем сообщение пользователя
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Не удалось удалить сообщение пользователя: {e}")

    # Отправляем сообщение от имени бота
    await message.answer(
        "📸 Отправьте фото, но не более 10 штук",
        reply_markup=keyboard_start_menu()
    )

    await state.set_state(States.video)


@router.message(StateFilter(States.video))
async def send_video_handler(message: Message, state: FSMContext):
    """
    Сохраняет фото и просит пользователя отправить видео.
    """
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"Не удалось удалить сообщение с фото: {e}")

    await message.answer(
        "🎥 Отправьте видео, но не более 1 штуки",
        reply_markup=keyboard_video_handler()
    )

    await state.set_state(States.sending)


@router.callback_query(F.data == "skip_step")
async def skip_step(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback_query.from_user.id
    table_size = data.get("size", "unknown")
    readable = TABLE_SIZES_NOX.get(table_size, "❓ Неизвестный размер")
    feedback_text = data.get("feedback", "⛔ Отзыв отсутствует")

    # Сохраняем в базу данных
    Review.create(
        user_id=user_id,
        table_size=readable,
        feedback_status="skipped_video",  # укажи явно статус
        feedback_text=feedback_text
    )

    logger.success(f"✅ [{user_id}] Отзыв сохранён (без видео): size={readable}, text={feedback_text}")

    # Отправляем сообщение админу
    admin_text = (
        f"📥 <b>Новый отзыв (без видео)</b>\n\n"
        f"👤 Пользователь: <code>{user_id}</code>\n"
        f"📏 Размер стола: {readable}\n"
        f"💬 Отзыв:\n{feedback_text}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML")

    # Ответ пользователю
    await callback_query.message.edit_text("🎉 Спасибо за ваш отзыв! Он был успешно сохранён 🙌")
    await state.clear()


@router.message(StateFilter(States.sending))
async def send_review_nox(message: Message, state: FSMContext):
    """
    Обработка нажатия на кнопку "Отправить".
    Сохраняет все данные в базу и завершает процесс.
    """
    data = await state.get_data()
    user_id = message.from_user.id
    table_size = data.get("size", "unknown")
    readable = TABLE_SIZES_NOX.get(table_size, "❓ Неизвестный размер")
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

    # Отправляем сообщение админу
    admin_text = (
        f"📥 <b>Новый отзыв</b>\n\n"
        f"👤 Пользователь: <code>{user_id}</code>\n"
        f"📏 Размер стола: {readable}\n"
        f"💬 Отзыв:\n{feedback_text}"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="HTML")

    # Сообщение пользователю
    await message.answer("🎉 Спасибо за ваш отзыв! Он был успешно сохранён 🙌")
    await state.clear()


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(the_nox_table)  # Регистрация обработчика
    router.callback_query.register(select_size_nox)  # Регистрация обработчика
    router.callback_query.register(send_review_nox)  # Регистрация обработчика
