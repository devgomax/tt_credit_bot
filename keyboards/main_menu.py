from aiogram import types

from buttons.inline_buttons import InlineButtons

buttons_list = [
    [InlineButtons.CREDITS.value],
    [InlineButtons.SUPPORT.value]
]
main_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons_list)
