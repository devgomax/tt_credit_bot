from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from keyboards import back_markup
from loader import dp
from states import NewCreditStates, ReportStates


@dp.message_handler(state=ReportStates.attachment)
async def wrong_file_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await data['prev'].delete()
    except MessageToDeleteNotFound:
        pass
    msg = await message.answer(text='Сообщение должно содержать только фото',
                               reply_markup=back_markup)
    await state.update_data({'prev': msg})


@dp.message_handler(state=NewCreditStates.credit_sum)
async def non_decimal_credit_sum_handler(message: types.Message,
                                         state: FSMContext):
    data = await state.get_data()
    try:
        await data['prev'].delete()
    except MessageToDeleteNotFound:
        pass
    await message.answer(
        text='Сумма должна содержать только числовое значение',
        reply_markup=back_markup
    )
