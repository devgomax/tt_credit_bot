from aiogram import types
from aiogram.dispatcher import FSMContext

from buttons.inline_buttons import InlineButtons
from keyboards import main_markup
from loader import dp

back_cb_data = InlineButtons.BACK.value.callback_data


@dp.callback_query_handler(text=back_cb_data, state='*')
async def back_to_main_menu_handler(query: types.CallbackQuery,
                                    state: FSMContext):
    await state.finish()
    await query.message.edit_text(text='Выберите действие',
                                  reply_markup=main_markup)
