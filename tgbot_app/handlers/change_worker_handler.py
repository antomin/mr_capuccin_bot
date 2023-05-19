import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards import (cancel_state_kb, changing_cd,
                                 gen_start_changing_kb, gen_tasks_kb)
from tgbot_app.loader import bot, dp
from tgbot_app.utils.db_api import (change_work_session_worker, get_worker,
                                    user_is_busy, get_work_session)
from tgbot_app.utils.text_variables import (CHANGE_USER_BUSY_TEXT,
                                            CHANGE_USER_OK_TEXT,
                                            CHANGING_ASK_ID_TEXT,
                                            CHANGING_CONFIRM_TXT,
                                            CHANGING_NEW_WORKER_TEXT,
                                            CHANGING_NO_WORKER_TEXT,
                                            WRONG_ID_TEXT)


@dp.message_handler(Command('change'))
async def start_changing(message: Message):
    work_session = await get_work_session(message.from_user.id)

    if not work_session:
        await message.answer('Вы не находитесь на смене.')
        return

    markup = await gen_start_changing_kb()
    await message.answer(text=CHANGING_CONFIRM_TXT, reply_markup=markup)


@dp.callback_query_handler(changing_cd.filter(action='cancel'))
async def cancel_changing(callback: CallbackQuery):
    markup = await gen_tasks_kb(user_id=callback.from_user.id)
    await callback.message.answer(text='Отменено', reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(changing_cd.filter(action='confirm'))
async def confirm_changing(callback: CallbackQuery, state: FSMContext):
    cancel_markup = await cancel_state_kb()
    await state.set_state('wait_user_id_for_changing')

    await callback.message.answer(CHANGING_ASK_ID_TEXT, reply_markup=cancel_markup)
    await callback.answer()


@dp.message_handler(state='wait_user_id_for_changing')
async def create_changing(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cancel_markup = await cancel_state_kb()

    if not message.text.isdigit():
        await message.answer(text=WRONG_ID_TEXT, reply_markup=cancel_markup)
        return

    new_worker_id = int(message.text)
    new_worker = await get_worker(new_worker_id)
    old_worker = await get_worker(user_id)

    if not new_worker:
        await message.answer(CHANGING_NO_WORKER_TEXT, reply_markup=cancel_markup)
        return

    if await user_is_busy(new_worker_id):
        text = CHANGE_USER_BUSY_TEXT.format(new_worker)
        await message.answer(text=text, reply_markup=cancel_markup)
        return

    if await change_work_session_worker(old_user_id=user_id, new_user_id=new_worker_id):
        await asyncio.sleep(1)
        await message.answer(CHANGE_USER_OK_TEXT)

        markup = await gen_tasks_kb(new_worker_id)
        text = CHANGING_NEW_WORKER_TEXT.format(old_worker)
        await bot.send_message(chat_id=new_worker_id, text=text, reply_markup=markup)
        await state.reset_state()
