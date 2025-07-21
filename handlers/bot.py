from aiogram import F
from aiogram.types import CallbackQuery
from loguru import logger

from dispatcher import router

# ID канала или группы для публикации отзывов
CHANNEL_ID = "@tehnik_shanel"


@router.callback_query(F.data == "to_publish")
async def handle_publish(callback: CallbackQuery):
    try:
        # Пересылаем сообщение, на которое был reply (то есть отзыв с медиа)
        replied_message = callback.message.reply_to_message
        if replied_message:
            await replied_message.forward(CHANNEL_ID)
            await callback.message.edit_text("✅ Отзыв опубликован!")
            logger.info(f"Отзыв опубликован админом {callback.from_user.id}")
        else:
            await callback.message.answer("❌ Ошибка: не найдено сообщение для публикации.")
    except Exception as e:
        logger.error(f"Ошибка при публикации: {e}")
        await callback.message.answer("❌ Произошла ошибка при публикации.")


@router.callback_query(F.data == "do_not_publish")
async def handle_reject(callback: CallbackQuery):
    try:
        # Удаляем сообщение с кнопками (и, если нужно, сам отзыв — можно добавить)
        await callback.message.edit_text("❌ Отзыв отклонён модератором.")
        logger.info(f"Отзыв отклонён админом {callback.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отклонении: {e}")
        await callback.message.answer("❌ Произошла ошибка при отклонении.")


def register_handlers_publish():
    router.callback_query.register(handle_publish)  # Регистрация обработчика
    router.callback_query.register(handle_reject)  # Регистрация обработчика
