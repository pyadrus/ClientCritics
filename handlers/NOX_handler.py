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

from dispatcher import router, bot, ID_GROUP
from keyboards.NOX_keyboards import (selection_size_arbo_primo_table_keyboard_nox, TABLE_SIZES_NOX, keyboard_start_menu,
                                     keyboard_confirm_or_cancel)
from messages.messages import size_selection_text
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
    size_key = TABLE_SIZES_NOX.get(size_key)
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
    feedback_text = data.get("feedback")
    table_size = data.get("size")

    text = (
        f"📦 Стол: ARBO NOX\n"
        f"Размер: {table_size}\n"
        f"✍️ Отзыв: {feedback_text}\n"
    )

    # Если это часть альбома
    if message.media_group_id:
        album_buffer[message.media_group_id].append(message)
        await asyncio.sleep(1.5)

        # Удаляем старое сообщение бота (например: "📸 Отправьте фото и видео...")
        last_bot_message_id = data.get("last_bot_message_id")
        if last_bot_message_id:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
            except Exception as e:
                logger.warning(f"Не удалось удалить предыдущее сообщение бота: {e}")

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

            media_group = []
            for idx, pid in enumerate(photo_ids):
                media_group.append(InputMediaPhoto(media=pid, caption=text if idx == 0 else None))
            for idx, vid in enumerate(video_ids):
                media_group.append(
                    InputMediaVideo(media=vid, caption=text if not photo_ids and idx == 0 else None))
            if media_group:
                await message.answer_media_group(media_group)
            confirm_msg = await message.answer("🔎 Проверьте отзыв перед отправкой. Всё верно?",
                                               reply_markup=keyboard_confirm_or_cancel())
            await state.update_data(last_bot_message_id=confirm_msg.message_id)
            await state.set_state(States.sending)
    else:
        # Обработка одиночного медиа
        if data.get("photo_response_sent"):
            return

        # Удаляем старое сообщение бота (например: "📸 Отправьте фото и видео...")
        last_bot_message_id = data.get("last_bot_message_id")
        if last_bot_message_id:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
            except Exception as e:
                logger.warning(f"Не удалось удалить предыдущее сообщение бота: {e}")

        # Удаляем предыдущее сообщение бота
        last_bot_message_id = data.get("last_bot_message_id")
        if last_bot_message_id:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
        if message.photo:
            photo_id = message.photo[-1].file_id
            photo_ids = data.get("photo_ids", [])
            photo_ids.append(photo_id)
            await state.update_data(photo_ids=photo_ids, photo_response_sent=True)
            media = [InputMediaPhoto(media=photo_id, caption=text)]
            await message.answer_media_group(media)
        elif message.video:
            video_id = message.video.file_id
            video_ids = data.get("video_ids", [])
            video_ids.append(video_id)
            await state.update_data(video_ids=video_ids, photo_response_sent=True)
            await message.answer_video(video_id, caption=text)
        else:
            await message.answer(text)
        confirm_msg = await message.answer("🔎 Проверьте отзыв перед отправкой. Всё верно?",
                                           reply_markup=keyboard_confirm_or_cancel())
        await state.update_data(last_bot_message_id=confirm_msg.message_id)
        await state.set_state(States.sending)


@router.callback_query(F.data == "confirm_review")
async def handle_review_confirmation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    table_size = data.get("size", "unknown")
    readable = TABLE_SIZES_NOX.get(table_size, "❓ Неизвестный размер")
    feedback_text = data.get("feedback", "")
    photo_ids = data.get("photo_ids", [])
    video_ids = data.get("video_ids", [])

    logger.success(f"✅ [{callback.from_user.id}] Отзыв подтверждён и отправлен на модерацию")

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    # Отправка в группу на модерацию
    await send_review_to_user_and_admin(
        user_id=callback.from_user.id,
        message=callback.message,
        readable=readable,
        feedback_text=feedback_text,
        photo_ids=photo_ids,
        video_ids=video_ids,
        target_chat_id=ID_GROUP  # 👈 добавим параметр
    )

    await callback.message.answer("🎉 Спасибо! Ваш отзыв отправлен на модерацию 👀", reply_markup=keyboard_start_menu())
    await state.clear()


# 📸 Универсальная функция отправки отзыва
async def send_review_to_user_and_admin(user_id, message, readable, feedback_text, photo_ids, video_ids=None,
                                        target_chat_id=None):
    chat_id = target_chat_id or message.chat.id  # если не задан, шлём пользователю

    # 1. Текст перед медиа
    await bot.send_message(
        chat_id=chat_id,
        text=f"📩 Новый отзыв от пользователя {user_id}!\n\n📦 Стол: {readable}\n✍️ Отзыв:\n{feedback_text}",
    )

    # 2. Собираем общий альбом
    media_group = []
    if photo_ids:
        for idx, pid in enumerate(photo_ids):
            media_group.append(InputMediaPhoto(media=pid, caption=feedback_text if idx == 0 else None))

    if video_ids:
        for idx, vid in enumerate(video_ids):
            # Если нет фото и это первое видео — добавим подпись
            media_group.append(InputMediaVideo(media=vid, caption=feedback_text if not photo_ids and idx == 0 else None))

    # 3. Отправляем альбомом (если что-то есть)
    if media_group:
        await bot.send_media_group(chat_id=chat_id, media=media_group)

    # 4. Если не было фото/видео — отправим только текст
    if not media_group:
        await bot.send_message(chat_id=chat_id, text=f"✍️ Отзыв:\n{feedback_text}")


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(handle_nox_table_selection)  # Регистрация обработчика
    router.callback_query.register(handle_nox_size_selected)  # Регистрация обработчика
    router.message.register(handle_feedback_text_received)  # Регистрация обработчика
    router.message.register(handle_media_group)  # Регистрация обработчика

# 205
