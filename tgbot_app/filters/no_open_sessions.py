from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards import gen_tasks_kb
from tgbot_app.utils.db_api import get_work_session
from tgbot_app.utils.text_variables import OPEN_SESSION_FILTER_TEXT


class NoOpenSessions(BoundFilter):
    async def check(self, message: Message | CallbackQuery) -> bool:
        user_id = message.from_user.id
        work_session = await get_work_session(user_id=user_id)
        if work_session:
            if isinstance(message, CallbackQuery):
                await message.answer(OPEN_SESSION_FILTER_TEXT, show_alert=True)
            else:
                markup = await gen_tasks_kb(user_id)
                await message.answer(OPEN_SESSION_FILTER_TEXT, reply_markup=markup)
            return False
        return True


