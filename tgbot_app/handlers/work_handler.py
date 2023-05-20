import hashlib

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from django.conf import settings

from tgbot_app.filters import NoOpenSessions
from tgbot_app.keyboards import (cancel_state_kb, gen_confirm_store_kb,
                                 gen_stores_kb, gen_tasks_kb, store_cd,
                                 task_cd)
from tgbot_app.loader import dp, scheduler
from tgbot_app.shedulers import change_tasks_scheduler
from tgbot_app.utils.common import get_dt_for_scheduler
from tgbot_app.utils.db_api import (check_img_unique, confirm_task,
                                    create_work_session, get_store, get_task,
                                    get_worker, need_confirm)
from tgbot_app.utils.text_variables import (CONFIRMATION_TEXT,
                                            NOT_UNIQUE_PHOTO_TEXT,
                                            OPEN_WORK_SESSION_TEXT,
                                            OUT_OF_TIME_TEXT,
                                            PHOTO_CONFIRMATION_OK,
                                            SELECT_STORE_TEXT, START_WORK_TEXT)


@dp.callback_query_handler(lambda callback: callback.data == 'start_work', NoOpenSessions())
@dp.message_handler(Command('start_work'), NoOpenSessions())
async def select_store_handler(message: Message | CallbackQuery):
    user_id = message.from_user.id
    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message

    worker = await get_worker(user_id)
    text = START_WORK_TEXT.format(worker.first_name)
    markup = await gen_stores_kb()

    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(store_cd.filter(action='start'), NoOpenSessions())
async def confirm_store_handler(callback: CallbackQuery, callback_data: dict):
    store_id = callback_data.get('store_id')
    store = await get_store(store_id)
    text = SELECT_STORE_TEXT.format(store.title)
    markup = await gen_confirm_store_kb(store_id)

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(store_cd.filter(action='confirm'), NoOpenSessions())
async def start_work_handler(callback: CallbackQuery, callback_data: dict):
    store_id = callback_data.get('store_id')
    user_id = callback.from_user.id
    store = await get_store(store_id=store_id)
    time_exec_str = await store.get_time_exec('morning')
    text = OPEN_WORK_SESSION_TEXT.format(time_exec_str.strftime('%H:%M'))

    work_session_id = await create_work_session(store_id=store_id, user_id=user_id)

    times = await get_dt_for_scheduler(store=store)

    for time_exec in ('morning', 'midday', 'evening'):
        scheduler.add_job(change_tasks_scheduler, trigger='date', run_date=times[time_exec],
                          kwargs={'work_session_id': work_session_id, 'time_exec': time_exec})

    markup = await gen_tasks_kb(user_id=user_id)

    await callback.message.answer(text=text, reply_markup=markup)
    await callback.answer()


@dp.callback_query_handler(task_cd.filter())
async def complete_task(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    task_id = callback_data.get('task_id')
    task = await get_task(task_id=task_id)

    if task.is_completed:
        await callback.answer()
        return

    if task.out_of_time:
        await callback.answer(OUT_OF_TIME_TEXT, show_alert=True)
        return

    if await need_confirm(task):
        cancel_markup = await cancel_state_kb()
        await state.set_state('waiting_img')
        async with state.proxy() as data:
            data['task_id'] = task_id
        await callback.message.answer(text=CONFIRMATION_TEXT, reply_markup=cancel_markup)
        await callback.answer()
        return

    await confirm_task(task_id=task_id)

    markup = await gen_tasks_kb(callback.from_user.id)

    await callback.message.edit_reply_markup(markup)


@dp.message_handler(state='waiting_img', content_types=['photo'])
async def check_img_confirmation(message: Message, state: FSMContext):
    cancel_markup = await cancel_state_kb()
    if not message.photo:
        await message.answer(text=CONFIRMATION_TEXT, reply_markup=cancel_markup)
        return

    photo = message.photo[-1]
    path = f'{settings.MEDIA_ROOT}/confirmations/{photo.file_id}.jpg'
    await photo.download(destination_file=path)

    with open(path, 'rb') as file:
        data = file.read()
        md5 = hashlib.md5(data).hexdigest()

    if not await check_img_unique(md5):
        await message.answer(text=NOT_UNIQUE_PHOTO_TEXT, reply_markup=cancel_markup)
        return

    async with state.proxy() as data:
        task_id = data.get('task_id')

    await confirm_task(task_id=task_id, path_img=f'confirmations/{photo.file_id}.jpg', md5_img=md5)

    markup = await gen_tasks_kb(user_id=message.from_user.id)

    await message.answer(text=PHOTO_CONFIRMATION_OK, reply_markup=markup)
    await state.reset_state()
