from aiogram.dispatcher.filters.state import State, StatesGroup


class ReportStates(StatesGroup):
    support = State()
    report = State()
    attachment = State()
