# -*- coding: utf-8 -*-
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
TOKEN = os.getenv("BOT_TOKEN")  # Токен бота
ID_GROUP = os.getenv("ID_GROUP") # ID группы в телеграм, для пересылки сообщений

ADMIN_ID = 535185511  # ID администратора

dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()
dp.include_router(router)
