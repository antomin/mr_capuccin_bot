from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from tgbot_app.utils.db_api import get_workers_id
from tgbot_app.utils.text_variables import WRONG_USER_TEXT


class IsWorkerMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, cb_data: dict):
        if message.text in ('/start', '/info'):
            return
        workers_id = await get_workers_id()
        if message.from_user.id not in workers_id:
            await message.answer(WRONG_USER_TEXT)
            raise CancelHandler()
