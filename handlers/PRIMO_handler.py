# -*- coding: utf-8 -*-
import asyncio
import json
import os
from collections import defaultdict

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import InputMediaPhoto
from aiogram.types import InputMediaVideo  # Добавь в импорты
from loguru import logger

from dispatcher import router, bot, ID_GROUP
from keyboards.keyboards import (selection_size_table_keyboard, TABLE_SIZES_NOX, selection_colour_keyboard, COLOURS,
                                 keyboard_start_menu, keyboard_confirm_or_cancel_primo, admin_keyboard)
from messages.messages import size_selection_text, review_prompt_text, table_color_prompt_text, media_upload_prompt
from states.states import StatesPrimo
from utils.media import process_single_photo, process_single_video

# Словарь временного хранения альбомов
album_buffer = defaultdict(list)  # media_group_id -> List[Message]
published_media_cache = {}


# 1. Выбор размера
@router.callback_query(F.data == "arbo_primo_table")
async def handle_primo_table_selection(callback: CallbackQuery, state: FSMContext):
    """
    📌 Обработчик нажатия на кнопку "Стол ARBO PRIMO".
    Показывает пользователю клавиатуру выбора размера стола.
    """
    await callback.message.edit_text(size_selection_text, reply_markup=selection_size_table_keyboard())
    logger.warning("Пользователь нажал кнопку 'Стол ARBO PRIMO'")
    await state.set_state(StatesPrimo.size_primo)


# 2. Выбор цвета (после выбора размера)
@router.callback_query(StateFilter(StatesPrimo.size_primo), F.data.in_(TABLE_SIZES_NOX.keys()))
async def handle_primo_size_selected(callback: CallbackQuery, state: FSMContext):
    """
    ✍️ Пользователь выбрал размер стола.
    Сохраняем размер и переходим к выбору цвета.
    """
    size_key = callback.data
    size_value = TABLE_SIZES_NOX.get(size_key)
    await state.update_data(size=size_value)  # Используется ключ "size"
    logger.warning(f"Пользователь выбрал размер {size_value}")
    # Удаляем предыдущее сообщение
    await callback.message.delete()
    # Отправляем сообщение с выбором цвета
    msg = await callback.message.answer(table_color_prompt_text, reply_markup=selection_colour_keyboard())
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(StatesPrimo.colour_primo)


# 3. Получение отзыва (после выбора цвета)
@router.callback_query(StateFilter(StatesPrimo.colour_primo), F.data.in_(COLOURS.keys()))
async def select_colour_primo(callback_query: CallbackQuery, state: FSMContext):
    """
    🎨 Пользователь выбрал цвет.
    Сохраняем цвет и запрашиваем текст отзыва.
    """
    colour_key = callback_query.data
    colour_value = COLOURS.get(colour_key)
    await state.update_data(colour=colour_value)  # Используется ключ "colour"
    logger.warning(f"Пользователь выбрал цвет {colour_value}")
    # Удаляем сообщение с выбором цвета
    await callback_query.message.delete()
    # Запрашиваем текст отзыва
    msg = await callback_query.message.answer(review_prompt_text, reply_markup=keyboard_start_menu())
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(StatesPrimo.feedback_primo)


# 4. Прием фото и видео (после ввода текста отзыва)
@router.message(StateFilter(StatesPrimo.feedback_primo))
async def handle_feedback_text_received_primo(message: Message, state: FSMContext):
    """
    Сохраняет отзыв и просит пользователя отправить фото.
    """
    await state.update_data(feedback=message.text.strip())  # Сохраняем текст отзыва, используя ключ "feedback"
    # Удаляем сообщение пользователя
    await message.delete()
    logger.warning(f"Пользователь отправил отзыв {message.text.strip()}")
    # Удаляем старое сообщение бота (📝 Напишите ваш отзыв в сообщении 👇)
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")
    if last_bot_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
    # Отправляем сообщение от имени бота
    msg = await message.answer(media_upload_prompt, reply_markup=keyboard_start_menu())
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(StatesPrimo.photo_video_primo)


# 5. Обработка фото и видео
@router.message(StateFilter(StatesPrimo.photo_video_primo), F.photo | F.video)
async def handle_media_group_primo(message: Message, state: FSMContext):
    data = await state.get_data()
    # ✅ Исправлено: используем правильные ключи
    feedback_text = data.get("feedback")  # Правильный ключ
    table_size = data.get("size")  # Правильный ключ
    colour = data.get("colour")  # Правильный ключ
    text = (
        f"📦 Стол: ARBO PRIMO\n"
        f"📏 Размер: {table_size}\n"
        f"🎨 Цвет: {colour}\n"
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
        album = album_buffer[message.media_group_id]
        if album and album[-1].message_id == message.message_id:
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
                media_msgs = await message.answer_media_group(media_group)
                if media_msgs:
                    preview_ids = [msg.message_id for msg in media_msgs]
                    await state.update_data(preview_message_ids=preview_ids)
            confirm_msg = await message.answer("🔎 Проверьте отзыв перед отправкой. Всё верно?",
                                               reply_markup=keyboard_confirm_or_cancel_primo())
            await state.update_data(last_bot_message_id=confirm_msg.message_id)
    else:
        preview_ids = []

        if message.photo:
            preview_ids = await process_single_photo(message, state, data, text)
        elif message.video:
            preview_ids = await process_single_video(message, state, data, text)
        else:
            await message.answer(text)
        await state.update_data(preview_message_ids=preview_ids)
        confirm_msg = await message.answer("🔎 Проверьте отзыв перед отправкой. Всё верно?",
                                           reply_markup=keyboard_confirm_or_cancel_primo())
        await state.update_data(last_bot_message_id=confirm_msg.message_id)


@router.callback_query(F.data == "confirm_review_primo")
async def handle_review_confirmation_primo(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # ✅ Исправлено: используем правильные ключи
    table_size = data.get("size")  # Правильный ключ
    colour = data.get("colour")  # Правильный ключ
    feedback_text = data.get("feedback", "")  # Правильный ключ
    photo_ids = data.get("photo_ids", [])
    video_ids = data.get("video_ids", [])
    logger.success(f"✅ [{callback.from_user.id}] Отзыв подтверждён и отправлен на модерацию")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    # Удаляем сообщение с предварительным просмотром отзыва (медиа или текст)
    preview_ids = data.get("preview_message_ids", [])
    for mid in preview_ids:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=mid)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение с медиа id={mid}: {e}")
    await send_review_to_user_and_admin_primo(
        user=callback.from_user,  # Передаем весь объект пользователя
        message=callback.message,
        table_size=table_size,
        colour=colour,  # Цвет стола
        feedback_text=feedback_text,
        photo_ids=photo_ids,
        video_ids=video_ids,
        target_chat_id=ID_GROUP
    )
    await callback.message.answer("🎉 Спасибо! Ваш отзыв отправлен на модерацию 👀", reply_markup=keyboard_start_menu())
    await state.clear()


# 📸 Универсальная функция отправки отзыва
async def send_review_to_user_and_admin_primo(user, message, table_size, colour, feedback_text, photo_ids,
                                              video_ids=None,
                                              target_chat_id=None):
    chat_id = target_chat_id or message.chat.id  # если не задан, шлём пользователю

    # --- Формируем информацию о пользователе ---
    # Приоритет: username > Имя Фамилия > Имя > ID
    user_info_parts = []
    if user.first_name:
        user_info_parts.append(user.first_name)
    if user.last_name:
        user_info_parts.append(user.last_name)

    full_name = " ".join(user_info_parts).strip() if user_info_parts else ""

    if user.username:
        # Если есть username, показываем его с @
        user_display = f"@{user.username}"
    elif full_name:
        # Если есть имя/фамилия, показываем их
        user_display = full_name
    else:
        # Если ничего нет, показываем ID
        user_display = f"ID: {user.id}"

    text = (
        f"📩 Отзыв от пользователя {user_display}!\n"
        f"📦 Стол: ARBO PRIMO\n"
        f"📏 Размер стола: {table_size}\n"
        f"🎨 Цвет стола: {colour}\n"  # Добавили цвет
        f"✍️ Отзыв: {feedback_text}"
    )
    # 1. Собираем общий альбом
    media_group = []
    if photo_ids:
        for idx, pid in enumerate(photo_ids):
            media_group.append(InputMediaPhoto(media=pid, caption=text if idx == 0 else None))
    if video_ids:
        for idx, vid in enumerate(video_ids):
            media_group.append(InputMediaVideo(media=vid, caption=text if not photo_ids and idx == 0 else None))
    # 2. Отправляем альбомом (если есть медиа)
    if media_group:
        media_group = media_group[:10]  # Ограничение Telegram
        sent_messages = await bot.send_media_group(chat_id=chat_id, media=media_group)
        first_message_id = sent_messages[0].message_id  # <-- Сохраняем ID первого сообщения
        os.makedirs("pending_reviews", exist_ok=True)
        # Сохраняем JSON с именем файла по ID первого сообщения
        json_path = os.path.join("pending_reviews", f"{first_message_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "photos": photo_ids,
                "videos": video_ids,
                "text": text,
                "user_id": user.id
            }, f, ensure_ascii=False, indent=2)
        # 3. Навешиваем клавиатуру на первое сообщение из альбома
        await bot.send_message(
            chat_id=chat_id,
            text="Выберите действие:",
            reply_to_message_id=first_message_id,  # <-- reply на первое сообщение
            reply_markup=admin_keyboard()
        )
    # 4. Если нет фото/видео — отправляем только текст с клавиатурой
    else:
        sent_message = await bot.send_message(chat_id=chat_id, text=text)  # <-- Сохраняем отправленное сообщение
        message_id_to_reply = sent_message.message_id  # <-- Получаем его ID
        os.makedirs("pending_reviews", exist_ok=True)
        # Сохраняем JSON с именем файла по ID отправленного сообщения
        json_path = os.path.join("pending_reviews", f"{message_id_to_reply}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "photos": photo_ids,
                "videos": video_ids,
                "text": text,
                "user_id": user.id
            }, f, ensure_ascii=False, indent=2)
        await bot.send_message(
            chat_id=chat_id,
            text="Выберите действие:",
            reply_to_message_id=message_id_to_reply,  # <-- reply на отправленное сообщение
            reply_markup=admin_keyboard()
        )


def register_PRIMO_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(handle_primo_table_selection)  # Регистрация обработчика
    router.callback_query.register(handle_primo_size_selected)  # Регистрация обработчика
    router.callback_query.register(select_colour_primo)  # Регистрация обработчика
    router.message.register(handle_feedback_text_received_primo)  # Регистрация обработчика
    router.message.register(handle_media_group_primo)  # Регистрация обработчика
    router.callback_query.register(handle_review_confirmation_primo)  # Регистрация обработчика
