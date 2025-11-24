# bot/main.py

import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import router
from core.auto_engine import AutoEngine
import os

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Register handlers
    dp.include_router(router)

    # Start AUTO MODE in background
    auto_engine = AutoEngine(bot, interval=180)  # 180 sec = 3 minutes
    asyncio.create_task(auto_engine.start())

    print("BOT IS RUNNING...")

    # Start bot polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
