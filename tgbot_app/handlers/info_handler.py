from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot_app.loader import dp


@dp.message_handler(Command('info'), state='*')
async def start_handler(message: Message, state: FSMContext):
    await state.reset_state()
    text = f'ID: {message.from_user.id}'
    await message.answer(text=text)
