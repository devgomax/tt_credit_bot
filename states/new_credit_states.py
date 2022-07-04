from aiogram.dispatcher.filters.state import State, StatesGroup


class NewCreditStates(StatesGroup):
    bank_name = State()
    credit_sum = State()
