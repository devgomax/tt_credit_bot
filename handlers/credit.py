from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from sqlmodel import select

from buttons.inline_buttons import InlineButtons
from database import Credit, Bank, get_session, get_or_create, get_all
from filters import IsDecimal
from keyboards import back_markup, credits_markup
from loader import dp
from states import NewCreditStates

credits_cb_data = InlineButtons.CREDITS.value.callback_data
add_credit_cb_data = InlineButtons.ADD_CREDIT.value.callback_data
calc_credit_cb_data = InlineButtons.CALCULATE_CREDIT.value.callback_data


# Работа с кредитами

@dp.callback_query_handler(text=credits_cb_data)
async def handle_credits_menu(query: types.CallbackQuery):
    await query.message.edit_text(text=InlineButtons.CREDITS.value.text,
                                  reply_markup=credits_markup)


# Добавить данные о новом кредите

@dp.callback_query_handler(text=add_credit_cb_data)
async def handle_add_credit_menu(query: types.CallbackQuery,
                                 state: FSMContext):
    await state.update_data(prev=query.message)
    await query.message.edit_text(text='Укажите наименование банка',
                                  reply_markup=back_markup)
    await NewCreditStates.bank_name.set()


@dp.message_handler(state=NewCreditStates.bank_name)
async def handle_bank_name(message: types.Message, state: FSMContext):
    msg = await message.answer(
        text='Укажите сумму кредита',
        reply_markup=back_markup,
    )
    async with state.proxy() as data:
        await data.get('prev').delete()
        data.update(bank_name=message.text, prev=msg)
    await NewCreditStates.credit_sum.set()


@dp.message_handler(IsDecimal(), state=NewCreditStates.credit_sum)
async def handle_credit_sum(message: types.Message, state: FSMContext):
    data = await state.get_data()
    session = next(get_session())
    bank = get_or_create(
        session, Bank, [('name', data.get('bank_name').lower())]
    )
    credit = get_or_create(session, Credit, [('bank_id', bank.id),
                                             ('user_id', message.from_user.id)])
    credit.summary += float(message.text)
    session.add_all([bank, credit])
    session.commit()
    try:
        await data.get('prev').delete()
    except MessageToDeleteNotFound:
        pass
    await message.answer(text='Информация по кредиту обновлена!',
                         reply_markup=back_markup)
    await state.finish()


# Рассчитать кредитный пакет в процентах

@dp.callback_query_handler(text=calc_credit_cb_data)
async def handle_credit_calculation(query: types.CallbackQuery):
    session = next(get_session())
    credits_list = get_all(session, Credit, [('user_id', query.from_user.id)])
    print(credits_list)
    total_amount = sum([credit.summary for credit in credits_list])
    message = f'Ваш кредитный пакет:\nОбщая сумма: {total_amount} у.е.\n'
    for credit in credits_list:
        bank = (session
                .exec(select(Bank).where(Bank.id == credit.bank_id))
                .one()
                )
        bank_info = f'{bank.name.title()}: ' \
                    f'{(credit.summary / total_amount) * 100:.3f} %'
        message += bank_info + '\n'
    await query.message.edit_text(text=message,
                                  reply_markup=back_markup)
