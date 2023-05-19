from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot_app.loader import dp


@dp.message_handler(Command('info'))
async def start_handler(message: Message):
    text = f'ID: {message.from_user.id}'
    await message.answer(text=text)
