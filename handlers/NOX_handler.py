# -*- coding: utf-8 -*-
import asyncio
from collections import defaultdict

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import InputMediaPhoto
from aiogram.types import InputMediaVideo  # Добавь в импорты
from loguru import logger

from dispatcher import router, bot, ADMIN_ID, ID_GROUP
from keyboards.NOX_keyboards import (selection_size_arbo_primo_table_keyboard_nox, TABLE_SIZES_NOX, keyboard_start_menu,
                                     keyboard_confirm_or_cancel)
from messages.messages import size_selection_text
from models.models import Review
from states.states import States

# Словарь временного хранения альбомов
album_buffer = defaultdict(list)  # media_group_id -> List[Message]


# 1. Выбор размера
@router.callback_query(F.data == "nox_table")
async def handle_nox_table_selection(callback: CallbackQuery, state: FSMContext):
    """
    📌 Обработчик нажатия на кнопку "Стол ARBO NOX".
    Показывает пользователю клавиатуру выбора размера стола.
    """
    await callback.message.edit_text(size_selection_text, reply_markup=selection_size_arbo_primo_table_keyboard_nox())
    logger.warning("Пользователь нажал кнопку 'Стол ARBO NOX'")
    await state.set_state(States.size)


# 2. Ввод текста отзыва
@router.callback_query(StateFilter(States.size), F.data.in_(TABLE_SIZES_NOX.keys()))
async def handle_nox_size_selected(callback: CallbackQuery, state: FSMContext):
    """
    ✍️ Пользователь нажал "Оставить отзыв".
    Переходим в состояние ожидания текстового отзыва.
    """
    size_key = callback.data
    await state.update_data(size=size_key)
    logger.warning(f"Пользователь выбрал размер {size_key}")
    msg = await callback.message.edit_text("📝 Напишите ваш отзыв в сообщении 👇", reply_markup=keyboard_start_menu())
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(States.feedback)


# 3. Прием фото и видео
@router.message(StateFilter(States.feedback))
async def handle_feedback_text_received(message: Message, state: FSMContext):
    """
    Сохраняет отзыв и просит пользователя отправить фото.
    """
    await state.update_data(feedback=message.text.strip())  # Сохраняем текст отзыва
    # Удаляем сообщение пользователя
    await message.delete()
    logger.warning(f"Пользователь отправил отзыв {message.text.strip()}")
    # Удаляем старое сообщение бота (📝 Напишите ваш отзыв в сообщении 👇)
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")
    if last_bot_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    # Отправляем сообщение от имени бота
    msg = await message.answer("📸 Отправьте фото и видео, но не более 10 штук", reply_markup=keyboard_start_menu())
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(States.photo_video)


# 3. Фото и альбомы
@router.message(StateFilter(States.photo_video), F.photo | F.video)
async def handle_media_group(message: Message, state: FSMContext):
    data = await state.get_data()

    # Если это часть альбома
    if message.media_group_id:
        album_buffer[message.media_group_id].append(message)
        await asyncio.sleep(1.5)

        if album_buffer[message.media_group_id][-1].message_id == message.message_id:
            messages = album_buffer.pop(message.media_group_id)
            logger.info(f"📸🎥 Получен альбом ({len(messages)} медиа) от пользователя {message.from_user.id}")

            photo_ids = []
            video_ids = []

            for msg in messages:
                await msg.delete()

                if msg.photo:
                    photo_ids.append(msg.photo[-1].file_id)
                elif msg.video:
                    video_ids.append(msg.video.file_id)

            await state.update_data(photo_ids=photo_ids, video_ids=video_ids, photo_response_sent=True)

            feedback_text = data.get("feedback_text", "✍️ Ваш отзыв")

            media_group = []
            for idx, pid in enumerate(photo_ids):
                media_group.append(InputMediaPhoto(media=pid, caption=feedback_text if idx == 0 else None))
            for idx, vid in enumerate(video_ids):
                media_group.append(
                    InputMediaVideo(media=vid, caption=feedback_text if not photo_ids and idx == 0 else None))

            if media_group:
                await message.answer_media_group(media_group)
            else:
                await message.answer(feedback_text)

            confirm_msg = await message.answer(
                "🔎 Проверьте отзыв перед отправкой. Всё верно?",
                reply_markup=keyboard_confirm_or_cancel()
            )
            await state.update_data(last_bot_message_id=confirm_msg.message_id)
            await state.set_state(States.sending)

    else:
        # Обработка одиночного медиа
        if data.get("photo_response_sent"):
            return

        # Удаляем предыдущее сообщение бота
        last_bot_message_id = data.get("last_bot_message_id")
        if last_bot_message_id:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
        feedback_text = data.get("feedback_text", "✍️ Ваш отзыв")
        if message.photo:
            photo_id = message.photo[-1].file_id
            photo_ids = data.get("photo_ids", [])
            photo_ids.append(photo_id)
            await state.update_data(photo_ids=photo_ids, photo_response_sent=True)
            media = [InputMediaPhoto(media=photo_id, caption=feedback_text)]
            await message.answer_media_group(media)
        elif message.video:
            video_id = message.video.file_id
            video_ids = data.get("video_ids", [])
            video_ids.append(video_id)
            await state.update_data(video_ids=video_ids, photo_response_sent=True)
            await message.answer_video(video_id, caption=feedback_text)
        else:
            await message.answer(feedback_text)
        confirm_msg = await message.answer(
            "🔎 Проверьте отзыв перед отправкой. Всё верно?",
            reply_markup=keyboard_confirm_or_cancel()
        )
        await state.update_data(last_bot_message_id=confirm_msg.message_id)
        await state.set_state(States.sending)


async def safe_delete(chat_id: int, message_id: int):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


async def retrieves_users_entered_data(state):
    """📦 Получение данных из FSM"""
    data = await state.get_data()
    table_size = data.get("size", "unknown")
    readable = TABLE_SIZES_NOX.get(table_size, "❓ Неизвестный размер")
    return (
        table_size,
        readable,
        data.get("feedback", "⛔ Отзыв отсутствует"),
        data.get("feedback", "no"),
        data.get("photo_ids", []),
        data.get("video_ids", []),  # ранее было video_id
    )


@router.callback_query(F.data == "confirm_review")
async def handle_review_confirmation(callback: CallbackQuery, state: FSMContext):
    table_size, readable, feedback_text, feedback_status, photo_ids, video_id = await retrieves_users_entered_data(
        state)
    # Сохраняем отзыв
    Review.create(user_id=callback.from_user.id, table_size=readable, feedback_status=feedback_status,
                  feedback_text=feedback_text, )
    logger.success(f"✅ [{callback.from_user.id}] Отзыв подтверждён и сохранён")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await send_review_to_user_and_admin(
        user_id=callback.from_user.id,
        message=callback.message,
        readable=readable,
        feedback_text=feedback_text,
        photo_ids=photo_ids,
        video_ids=video_id if isinstance(video_id, list) else ([video_id] if video_id else [])  # ✅
    )
    await state.clear()


# 📸 Универсальная функция отправки отзыва
async def send_review_to_user_and_admin(user_id, message, readable, feedback_text, photo_ids, video_ids=None):
    await bot.send_message(chat_id=ID_GROUP,
                           text=f"📩 Новый отзыв от пользователя {user_id}!\n\n📦 Стол: {readable}\n✍️ Отзыв:\n{feedback_text}", )
    if photo_ids:
        media = [InputMediaPhoto(media=pid) for pid in photo_ids]
        media[0].caption = feedback_text
        if len(media) == 1:
            await message.answer_photo(photo_ids[0], caption=feedback_text)
        else:
            await message.answer_media_group(media)
            await message.answer("⬆️ Это ваши фото отзыва\n\n👇 Что дальше?")

    if video_ids:
        media = [InputMediaVideo(media=vid) for vid in video_ids]
        if not photo_ids:
            media[0].caption = feedback_text
        await message.answer_media_group(media)

    if not photo_ids and not video_ids:
        await message.answer(f"✍️ Отзыв:\n{feedback_text}")

    await message.answer("🎉 Спасибо за ваш отзыв! Он был успешно сохранён 🙌", reply_markup=keyboard_start_menu())


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(handle_nox_table_selection)  # Регистрация обработчика
    router.callback_query.register(handle_nox_size_selected)  # Регистрация обработчика
    router.message.register(handle_feedback_text_received)  # Регистрация обработчика
    router.message.register(handle_media_group)  # Регистрация обработчика
