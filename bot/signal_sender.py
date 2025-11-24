# bot/signal_sender.py

import asyncio
from ai_engine import AIEngine
from data_feed import MarketData
from utils import format_signal_message


class SignalSender:
    def __init__(self, bot):
        self.bot = bot
        self.engine = AIEngine()
        self.data = MarketData()

        # Prevent spam signals
        self.last_signal_time = 0
        self.cooldown_seconds = 60  # 1 min between signals

    async def send_signal(self, chat_id):
        """Fetch data → generate signal → send to Telegram"""
        candles = await self.data.get_candles()

        if candles is None:
            await self.bot.send_message(chat_id, "⚠️ Unable to fetch market data.")
            return

        result = self.engine.generate_signal(candles)

        text = format_signal_message(result)

        await self.bot.send_message(chat_id, text)

    async def auto_loop(self, chat_id):
        """Background loop that sends signals repeatedly."""
        while True:
            try:
                await self.send_signal(chat_id)
                await asyncio.sleep(self.cooldown_seconds)

            except Exception as e:
                await self.bot.send_message(chat_id, f"⚠️ Error: {e}")
                await asyncio.sleep(3)
