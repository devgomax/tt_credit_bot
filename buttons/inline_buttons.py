from enum import Enum
from uuid import uuid4

from aiogram import types


class InlineButtons(Enum):
    CREDITS = types.InlineKeyboardButton(
        'Работа с кредитами',
        callback_data=uuid4().hex
    )
    ADD_CREDIT = types.InlineKeyboardButton(
        'Добавить данные о новом кредите',
        callback_data=uuid4().hex
    )
    CALCULATE_CREDIT = types.InlineKeyboardButton(
        'Рассчитать кредитный пакет в процентах',
        callback_data=uuid4().hex
    )
    BACK = types.InlineKeyboardButton(
        'Назад', callback_data=uuid4().hex
    )
    SUPPORT = types.InlineKeyboardButton(
        'Запрос в службу поддержки',
        callback_data=uuid4().hex
    )
    BUG_REPORT = types.InlineKeyboardButton(
        'Bug', callback_data='Bug'
    )
    FEATURE_REPORT = types.InlineKeyboardButton(
        'New feature', callback_data='New feature'
    )
    OTHER_REPORT = types.InlineKeyboardButton(
        'Other', callback_data='Other'
    )
