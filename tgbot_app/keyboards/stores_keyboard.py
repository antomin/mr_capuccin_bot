from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot_app.utils.db_api import get_current_tasks, get_store

store_cd = CallbackData('store', 'action', 'store_id')
task_cd = CallbackData('work', 'task_id')


async def gen_stores_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    stores = await get_store()

    async for store in stores:
        markup.insert(
            InlineKeyboardButton(text=store.title, callback_data=store_cd.new(store_id=store.id, action='start'))
        )

    return markup


async def gen_confirm_store_kb(store_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(InlineKeyboardButton(text='<<<', callback_data='start_work'))
    markup.insert(InlineKeyboardButton(text='Да', callback_data=store_cd.new(store_id=store_id, action='confirm')))

    return markup


async def gen_tasks_kb(user_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    tasks = await get_current_tasks(user_id=user_id)

    async for task in tasks:
        text = await task.get_title()
        if task.is_completed:
            text = '👌 ' + text
        markup.add(
            InlineKeyboardButton(text=text, callback_data=task_cd.new(task_id=task.id))
        )

    return markup
