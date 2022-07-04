from aiogram import types

from buttons.inline_buttons import InlineButtons

buttons_list = [
    [InlineButtons.ADD_CREDIT.value],
    [InlineButtons.CALCULATE_CREDIT.value],
    [InlineButtons.BACK.value]
]
credits_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons_list)
