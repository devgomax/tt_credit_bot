from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from buttons.inline_buttons import InlineButtons
from database import get_session
from database.reports import create_report
from keyboards import back_markup, report_markup
from loader import dp
from states import ReportStates
from utils.reports import save_report

support_cb_data = InlineButtons.SUPPORT.value.callback_data
bug_cb_data = InlineButtons.BUG_REPORT.value.callback_data
feature_cb_data = InlineButtons.FEATURE_REPORT.value.callback_data
other_cb_data = InlineButtons.OTHER_REPORT.value.callback_data


@dp.callback_query_handler(text=support_cb_data)
async def handle_support_menu(query: types.CallbackQuery):
    await query.message.edit_text(text='Выберите тип обращения',
                                  reply_markup=report_markup)
    await ReportStates.support.set()


@dp.callback_query_handler(text=bug_cb_data, state=ReportStates.support)
@dp.callback_query_handler(text=feature_cb_data, state=ReportStates.support)
@dp.callback_query_handler(text=other_cb_data, state=ReportStates.support)
async def handle_report_type(query: types.CallbackQuery, state: FSMContext):
    text = 'Опишите свой запрос одним сообщением'
    await query.message.edit_text(text, reply_markup=back_markup)
    await state.update_data({'type': query.data,
                             'prev': query.message})
    await ReportStates.report.set()


@dp.message_handler(state=ReportStates.report)
async def handle_report_text(message: types.Message, state: FSMContext):
    msg = await message.answer(
        text='Отправьте дополнительные вложения (только фото со сжатием) в '
             'одном сообщении',
        reply_markup=back_markup,
    )
    async with state.proxy() as data:
        await data.get('prev').delete()
        data.update(message=message.text, prev=msg)
    await ReportStates.attachment.set()


@dp.message_handler(is_media_group=True,
                    state=ReportStates.attachment,
                    content_types=types.ContentTypes.PHOTO)
async def handle_report_album_attachment(message: types.Message,
                                         album: list[types.Message],
                                         state: FSMContext):
    session = next(get_session())
    data = await state.get_data()
    try:
        data.get('prev').delete()
    except MessageToDeleteNotFound:
        pass
    file_urls = [
        await file.photo[-1].get_url() for file in album if file.photo
    ]
    data['file_url'] = ' '.join(file_urls)
    data['user_id'] = message.from_user.id
    report = create_report(session, data)
    await save_report(report.json())
    await message.answer(text='Обращение успешно сформировано!',
                         reply_markup=back_markup)
    await state.finish()


@dp.message_handler(state=ReportStates.attachment,
                    content_types=types.ContentTypes.PHOTO)
async def handle_report_single_attachment(message: types.Message,
                                          state: FSMContext):
    data = await state.get_data()
    session = next(get_session())
    try:
        data.get('prev').delete()
    except MessageToDeleteNotFound:
        pass
    data['file_url'] = await message.photo[-1].get_url()
    data['user_id'] = message.from_user.id
    report = create_report(session, data)
    await save_report(report.json())
    await message.answer(text='Обращение успешно сформировано!',
                         reply_markup=back_markup)
    await state.finish()
