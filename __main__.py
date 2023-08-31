import os

TOKEN = os.environ["BOT_TELETGRAM_TOKEN"]

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from model import Model

logging.basicConfig(level=logging.INFO)

async def start_bot() -> None:
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(handlers.dp)
    model = Model(os.environ["BOT_MONGODB_URL"], os.environ["BOT_MONGODB_NAME"],
                  os.environ["BOT_MODEL_SERVER_URL"])
    await dp.start_polling(bot, model=model)

if __name__ == "__main__": 
    asyncio.run(start_bot())
