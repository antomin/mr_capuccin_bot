import asyncio

from tgbot_app.keyboards import gen_tasks_kb
from tgbot_app.loader import bot
from tgbot_app.utils.db_api import change_tasks, get_store, get_work_session
from tgbot_app.utils.text_variables import (CHANGE_TASKS_TEXT,
                                            CLOSE_WORK_SESSION_TEXT)


async def change_tasks_scheduler(work_session_id: int, time_exec: str):
    work_session = await get_work_session(work_session_id=work_session_id)
    user_id = await work_session.get_worker_id()

    await change_tasks(work_session=work_session, time_exec=time_exec)
    await asyncio.sleep(1)

    if time_exec == 'evening':
        await bot.send_message(chat_id=user_id, text=CLOSE_WORK_SESSION_TEXT)
        return

    time_exec_rules = {'morning': 'midday', 'midday': 'evening'}
    store = await get_store(user_id=user_id)
    time_exec_str = await store.get_time_exec(time_exec=time_exec_rules[time_exec])
    markup = await gen_tasks_kb(user_id=user_id)

    await bot.send_message(chat_id=user_id, text=CHANGE_TASKS_TEXT.format(time_exec_str.strftime('%H:%M')),
                           reply_markup=markup)
