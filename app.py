from aiogram import Dispatcher

from database import init_db
from utils.commands import set_default_commands


async def on_startapp(dp: Dispatcher):
    dp.middleware.setup(AlbumMiddleware())
    await set_default_commands(dp)
    init_db()
    print('бот запущен')


if __name__ == '__main__':
    from aiogram import executor
    from aiogram.utils.exceptions import TelegramAPIError

    from handlers import dp
    from middlewares import AlbumMiddleware
    try:
        executor.start_polling(dp, on_startup=on_startapp, skip_updates=True)
    except TelegramAPIError as e:
        print(e)
