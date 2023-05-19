from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def cancel_state_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_state'))

    return markup
