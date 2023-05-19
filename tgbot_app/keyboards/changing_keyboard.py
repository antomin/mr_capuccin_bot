from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

changing_cd = CallbackData('changing', 'action')


async def gen_start_changing_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(InlineKeyboardButton(text='<<<', callback_data=changing_cd.new(action='cancel')))
    markup.insert(InlineKeyboardButton(text='Да', callback_data=changing_cd.new(action='confirm')))

    return markup
