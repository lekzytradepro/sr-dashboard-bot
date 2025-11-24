# bot/main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from bot.handlers import router as handlers_router
from core.scheduler import AutoEngine


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Register handlers
    dp.include_router(handlers_router)

    # Start auto signal engine (background task)
    auto_engine = AutoEngine(bot)
    asyncio.create_task(auto_engine.start())  # runs forever in background

    print("🚀 Bot is running...")

    # Start bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
