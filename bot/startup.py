# bot/startup.py
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.keyboards import register_keyboards
from bot.handlers import register_handlers
from bot.senders import register_senders


class BotStartup:
    def __init__(self, token: str):
        self.token = token
        self.bot = None
        self.dp = None

    async def initialize(self):
        """Initialize bot, dispatcher, handlers, and keyboards."""
        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()

        # Register keyboards
        register_keyboards(self.dp)

        # Register handlers
        register_handlers(self.dp)

        # Register senders (signal dispatchers, scheduled tasks)
        register_senders(self.dp, self.bot)

    async def start_polling(self):
        """Start bot polling process."""
        await self.dp.start_polling(self.bot)
