from aiogram import types
from buttons.inline_buttons import InlineButtons


buttons_list = [
    [InlineButtons.BUG_REPORT.value],
    [InlineButtons.FEATURE_REPORT.value],
    [InlineButtons.OTHER_REPORT.value],
    [InlineButtons.BACK.value]
]
report_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons_list)
