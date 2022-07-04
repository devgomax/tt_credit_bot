from pathlib import Path
from time import time

import aiofiles

MEDIA_DIR = Path(__file__).resolve().parent.parent / 'media'


async def save_report(data):
    async with aiofiles.open(f'{MEDIA_DIR}/{int(time())}.json', 'w+') as f:
        await f.write(data)
