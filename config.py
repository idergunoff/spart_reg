from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import types, executor
from aiogram.utils.exceptions import MessageCantBeDeleted, BadRequest, MigrateToChat, CantInitiateConversation, BotBlocked
from aiogram.utils import exceptions
from loguru import logger
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from emoji import emojize
from openpyxl import Workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color, PatternFill, Side, Border
import asyncio
import os
from datetime import datetime

from models import *
from button import *
import pytz

tz = pytz.timezone('Europe/Moscow')

super_admin = [325053382]

TOKEN = '5590505820:AAHdJNYfpJGiAmOfh8SRbFdpDWK9VdjDCZE' # тест


session = Session()

logger.add("logs/file_{time}.log", format="{time} - {level} - {message}", level="TRACE", rotation="7 day")


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
