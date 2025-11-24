import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.handlers import router as bot_router
from dashboard.middleware import register_dashboard_middleware

from config.keyboards import main_menu

# Load BOT TOKEN from environment
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # include bot handlers
    dp.include_router(bot_router)

    # include dashboard middleware
    register_dashboard_middleware(dp)

    # set bot menu
    await bot.set_my_commands(main_menu)

    print("🚀 Bot is running...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
