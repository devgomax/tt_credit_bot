from aiogram import types
from buttons.inline_buttons import InlineButtons


buttons_list = [
    [InlineButtons.BACK.value]
]
back_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons_list)
