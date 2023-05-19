from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

storage = MemoryStorage()
bot = Bot(token=settings.TGBOT_TOKEN, parse_mode='HTML', disable_web_page_preview=True)
dp = Dispatcher(bot=bot, storage=storage)
scheduler = AsyncIOScheduler()
