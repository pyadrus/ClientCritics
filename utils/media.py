from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def process_single_photo(message: Message, state: FSMContext, data: dict, text: str):
    """
    Обрабатывает одиночное фото: сохраняет file_id в состояние, отправляет фото с подписью,
    возвращает список id отправленного сообщения.
    :param message: Message - сообщение с фото
    :param state: FSMContext - состояние
    :param data: dict - данные
    :param text: str - подпись
    """
    preview_ids = []

    photo_id = message.photo[-1].file_id
    photo_ids = data.get("photo_ids", [])
    photo_ids.append(photo_id)
    await state.update_data(photo_ids=photo_ids, photo_response_sent=True)

    sent = await message.answer_photo(photo_id, caption=text)
    preview_ids.append(sent.message_id)

    return preview_ids


async def process_single_video(message: Message, state: FSMContext, data: dict, text: str):
    """
    Обрабатывает одиночное видео: сохраняет file_id в состояние, отправляет видео с подписью,
    возвращает список id отправленного сообщения.
    :param message: Message - сообщение с видео
    :param state: FSMContext - состояние
    :param data: dict - данные
    :param text: str - подпись
    :return: list - список id отправленных сообщений
    :return: list - список id отправленных сообщений
    """
    preview_ids = []

    video_id = message.video.file_id
    video_ids = data.get("video_ids", [])
    video_ids.append(video_id)
    await state.update_data(video_ids=video_ids, photo_response_sent=True)

    sent = await message.answer_video(video_id, caption=text)
    preview_ids.append(sent.message_id)

    return preview_ids
