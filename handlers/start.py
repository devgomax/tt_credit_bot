from aiogram import types
from aiogram.dispatcher import FSMContext

from database import get_session, User, get_or_create
from keyboards import main_markup
from loader import dp


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    session = next(get_session())
    get_or_create(session, User, [('id', message.from_user.id)])
    await message.reply(f'Welcome {message.from_user.full_name}!',
                        reply=False,
                        reply_markup=main_markup)
