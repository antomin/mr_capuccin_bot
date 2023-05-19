from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot_app.filters import NoOpenSessions
from tgbot_app.loader import dp
from tgbot_app.utils.text_variables import START_TEXT


@dp.message_handler(Command('start'), NoOpenSessions())
async def start_handler(message: Message):
    await message.answer(START_TEXT)
