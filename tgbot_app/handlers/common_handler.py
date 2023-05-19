from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot_app.keyboards import gen_tasks_kb
from tgbot_app.loader import dp


@dp.callback_query_handler(lambda callback: callback.data == 'cancel_state', state='*')
async def cancel_state_handler(callback: CallbackQuery, state: FSMContext):
    await state.reset_state()
    markup = await gen_tasks_kb(callback.from_user.id)

    await callback.message.answer(text='Отменено.', reply_markup=markup)
    await callback.answer()
