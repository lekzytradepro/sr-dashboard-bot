# bot/startup.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from core.config import settings
from bot.handlers import register_handlers

bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def start_bot():
    """
    Start Telegram bot, register handlers, and launch event loop.
    """
    print("🚀 Starting AI Signal Bot...")

    # Register all command/message handlers
    register_handlers(dp)

    # Start polling
    await dp.start_polling(bot)


def run():
    """
    Entry point for Render / Docker / Local Start.
    """
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Bot stopped.")
