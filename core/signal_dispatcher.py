# core/signal_dispatcher.py

import asyncio
from datetime import datetime

from engine.asset_detector import AssetDetector
from core.ai_signal_engine import AISignalEngine
from storage.user_storage import UserStorage
from ai_engine.reason_generator import ReasonGenerator
from ai_engine.signal_formatter import SignalFormatter

from aiogram import Bot


class SignalDispatcher:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.detector = AssetDetector()
        self.ai_engine = AISignalEngine()
        self.user_db = UserStorage()
        self.reason_engine = ReasonGenerator()
        self.format_engine = SignalFormatter()

    async def start_auto_signals(self):
        """
        Auto signal loop – finds best pair, generates the AI signal,
        builds the final message, and sends to all subscribers.
        """
        while True:
            asset = self.detector.get_best_pair()

            if asset is None:
                await asyncio.sleep(5)
                continue

            # Generate AI signal
            signal = self.ai_engine.generate_signal(asset)

            if signal["direction"] != "NEUTRAL":
                await self.send_to_all_users(signal)

            # Wait before the next signal
            await asyncio.sleep(60)

    async def send_to_all_users(self, signal):
        """Send the formatted signal to all active subscribers."""
        users = self.user_db.get_all_active_users()

        if not users:
            return

        msg = self.build_message(signal)

        for user in users:
            try:
                await self.bot.send_message(chat_id=user, text=msg, parse_mode="HTML")
            except:
                continue

    def build_message(self, signal: dict) -> str:
        """
        Builds the final message using:
        → ReasonGenerator
        → SignalFormatter
        """
        reason_text = self.reason_engine.build_reasons(signal)
        formatted = self.format_engine.format(
            pair=signal["asset"],
            direction=signal["direction"],
            confidence=signal["confidence"],
            indicators=signal["indicators"],
            reasons=reason_text,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return formatted
