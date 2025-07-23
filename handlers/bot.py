# -*- coding: utf-8 -*-
import json
import os

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto
from aiogram.types import InputMediaVideo  # Добавь в импорты
from loguru import logger

from dispatcher import bot, CHANNEL_ID
from dispatcher import router

# ID канала или группы для публикации отзывов

PENDING_DIR = "pending_reviews"

@router.callback_query(F.data == "to_publish")
async def handle_publish(callback: CallbackQuery):
    try:
        replied_message = callback.message.reply_to_message
        if not replied_message:
            await callback.message.answer("❌ Не найдено сообщение для публикации.")
            return

        message_id = replied_message.message_id
        json_path = os.path.join(PENDING_DIR, f"{message_id}.json")

        if not os.path.exists(json_path):
            await callback.message.answer("❌ Нет данных для публикации.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            media_data = json.load(f)

        text = media_data["text"]
        photo_ids = media_data["photos"]
        video_ids = media_data["videos"]

        media_group = []
        for idx, pid in enumerate(photo_ids):
            media_group.append(InputMediaPhoto(media=pid, caption=text if idx == 0 else None))
        for idx, vid in enumerate(video_ids):
            media_group.append(InputMediaVideo(media=vid, caption=text if not photo_ids and idx == 0 else None))

        media_group = media_group[:10]  # ограничение Telegram
        if media_group:
            await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=text)

        await callback.message.edit_text("✅ Отзыв опубликован!")
        logger.info(f"Опубликовано в канал: {callback.from_user.id}")

        # Удаляем json-файл
        os.remove(json_path)

    except Exception as e:
        logger.error(f"Ошибка при публикации: {e}")
        await callback.message.answer("❌ Произошла ошибка при публикации.")


@router.callback_query(F.data == "do_not_publish")
async def handle_reject(callback: CallbackQuery):
    try:
        replied_message = callback.message.reply_to_message
        if replied_message:
            message_id = replied_message.message_id
            json_path = os.path.join(PENDING_DIR, f"{message_id}.json")
            if os.path.exists(json_path):
                os.remove(json_path)

        await callback.message.edit_text("❌ Отзыв отклонён модератором.")
        logger.info(f"Отзыв отклонён админом {callback.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отклонении: {e}")
        await callback.message.answer("❌ Произошла ошибка при отклонении.")


def register_handlers_publish():
    router.callback_query.register(handle_publish)  # Регистрация обработчика
    router.callback_query.register(handle_reject)  # Регистрация обработчика
