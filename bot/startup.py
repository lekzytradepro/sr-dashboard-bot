# bot/startup.py

import asyncio
from aiogram import Bot, Dispatcher
from core.signal_dispatcher import SignalDispatcher
from config.global_config import BOT_TOKEN

async def start_bot():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Initialize the signal dispatcher
    signal_system = SignalDispatcher(bot)

    # Start auto signal loop
    asyncio.create_task(signal_system.start_auto_signals())

    print("🚀 Bot is running... Auto-signal system active.")
    return bot, dp
