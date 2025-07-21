# -*- coding: utf-8 -*-
import asyncio
from collections import defaultdict

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import InputMediaPhoto
from loguru import logger

from dispatcher import router, bot, ADMIN_ID
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
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"❗ Не удалось удалить сообщение: {e}")
    logger.warning(f"Пользователь отправил отзыв {message.text.strip()}")
    # Удаляем старое сообщение бота (📝 Напишите ваш отзыв в сообщении 👇)
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message_id")
    if last_bot_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение бота: {e}")
    # Отправляем сообщение от имени бота
    msg = await message.answer("📸 Отправьте фото и видео, но не более 10 штук", reply_markup=keyboard_start_menu())
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(States.photo_video)


# 3. Фото и альбомы
@router.message(StateFilter(States.photo_video), F.photo | F.video)
async def handle_media_group(message: Message, state: FSMContext):
    if message.media_group_id:
        album_buffer[message.media_group_id].append(message)
        await asyncio.sleep(1.5)
        # Последнее сообщение в альбоме
        if album_buffer[message.media_group_id][-1].message_id == message.message_id:
            messages = album_buffer.pop(message.media_group_id)
            logger.info(f"📸🎥 Получен альбом ({len(messages)} медиа) от пользователя {message.from_user.id}")
            # Удаляем все сообщения из чата
            for msg in messages:
                await msg.delete()
            # Сохраняем фото и видео
            photos = []
            video = None
            for msg in messages:
                if msg.photo:
                    photos.append(msg.photo[-1].file_id)
                elif msg.video:
                    video = msg.video.file_id
            # Обновляем состояние
            data = await state.get_data()
            await state.update_data(photo_ids=photos, video_id=video, photo_response_sent=True)
            # Удаляем предыдущее сообщение бота
            last_bot_message_id = data.get("last_bot_message_id")
            if last_bot_message_id:
                await safe_delete(message.chat.id, last_bot_message_id)
            # TODO ⚠️ Проверка на альбом. Упростить схему работы
            table_size, readable, feedback_text, feedback_status, photo_ids, video_id = await retrieves_users_entered_data(state)
            # Отправка предпросмотра отзыва пользователю
            if photo_ids:
                media = [InputMediaPhoto(media=pid) for pid in photo_ids]
                media[0].caption = feedback_text
                await message.answer_media_group(media)
            elif video_id:
                await message.answer_video(video_id, caption=feedback_text)
            else:
                await message.answer(f"✍️ Отзыв:\n{feedback_text}")
            # Кнопки подтверждения
            await message.answer("🔎 Проверьте отзыв перед отправкой. Всё верно?",
                                 reply_markup=keyboard_confirm_or_cancel())
            await state.update_data(last_bot_message_id=msg.message_id)
            await state.set_state(States.sending)

    else:  # Если нет альбома
        # Не альбом → как раньше
        data = await state.get_data()
        if data.get("photo_response_sent"):
            return
        # Удаляем старое сообщение бота
        last_bot_message_id = data.get("last_bot_message_id")
        if last_bot_message_id:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=last_bot_message_id)
            except Exception as e:
                logger.warning(f"Не удалось удалить сообщение бота: {e}")
        table_size, readable, feedback_text, feedback_status, photo_ids, video_id = await retrieves_users_entered_data(state)
        # Отправка предпросмотра отзыва пользователю
        if photo_ids:
            media = [InputMediaPhoto(media=pid) for pid in photo_ids]
            media[0].caption = feedback_text
            await message.answer_media_group(media)
        elif video_id:
            await message.answer_video(video_id, caption=feedback_text)
        else:
            await message.answer(f"✍️ Отзыв:\n{feedback_text}")
        # Кнопки подтверждения
        await message.answer("🔎 Проверьте отзыв перед отправкой. Всё верно?", reply_markup=keyboard_confirm_or_cancel())
        await state.update_data(last_bot_message_id=msg.message_id, photo_response_sent=True)
        # Сохраняем фото
        photo_id = message.photo[-1].file_id  # Получаем лучшее качество
        photo_list = data.get("photo_ids", [])
        photo_list.append(photo_id)
        await state.update_data(photo_ids=photo_list)
        await state.set_state(States.sending)


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
        data.get("video_id"),
    )


# 📸 Универсальная функция отправки отзыва
async def send_review_to_user_and_admin(user_id, message, readable, feedback_text, photo_ids, video_id = None):
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=f"📩 Новый отзыв от пользователя {user_id}!\n\n📦 Стол: {readable}\n✍️ Отзыв:\n{feedback_text}",)
    except Exception as e:
        logger.warning(f"❗ Ошибка при отправке админу: {e}")
    if photo_ids:
        media = [InputMediaPhoto(media=pid) for pid in photo_ids]
        media[0].caption = feedback_text
        if len(media) == 1:
            await message.answer_photo(photo_ids[0], caption=feedback_text)
        else:
            await message.answer_media_group(media)
            await message.answer("⬆️ Это ваши фото отзыва\n\n👇 Что дальше?")
    elif video_id:
        await message.answer_video(video_id, caption=feedback_text)
    await message.answer("🎉 Спасибо за ваш отзыв! Он был успешно сохранён 🙌", reply_markup=keyboard_start_menu())


@router.callback_query(F.data == "confirm_review")
async def handle_review_confirmation(callback: CallbackQuery, state: FSMContext):
    table_size, readable, feedback_text, feedback_status, photo_ids, video_id = await retrieves_users_entered_data(state)
    # Сохраняем отзыв
    Review.create(user_id=callback.from_user.id, table_size=readable, feedback_status=feedback_status, feedback_text=feedback_text,)
    logger.success(f"✅ [{callback.from_user.id}] Отзыв подтверждён и сохранён")
    try:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    except Exception as e:
        logger.warning(f"❗ Не удалось удалить сообщение {callback.message.message_id}: {e}")
    await send_review_to_user_and_admin(
        user_id=callback.from_user.id,
        message=callback.message,
        readable=readable,
        feedback_text=feedback_text,
        photo_ids=photo_ids,
        video_id=video_id
    )
    await state.clear()


def register_NOX_handlers():
    """Регистрация обработчиков"""
    router.callback_query.register(handle_nox_table_selection)  # Регистрация обработчика
    router.callback_query.register(handle_nox_size_selected)  # Регистрация обработчика
    router.message.register(handle_feedback_text_received)  # Регистрация обработчика
    router.message.register(handle_media_group)  # Регистрация обработчика
