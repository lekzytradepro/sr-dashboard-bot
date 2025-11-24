# core/auto_engine.py

import asyncio
from datetime import datetime
from engine.pair_detector import PairDetector
from engine.signal_storage import SignalEngine
from storage.user_storage import UserStorage
from bot.signal_sender import SignalSender
from aiogram import Bot

class AutoEngine:
    def __init__(self, bot: Bot, interval: int = 180):
        """
        interval = how often auto mode sends signals (seconds)
        180 = 3 minutes
        """
        self.bot = bot
        self.interval = interval
        self.user_storage = UserStorage()
        self.pair_detector = PairDetector()
        self.signal_engine = SignalEngine()

    async def start(self):
        """Main loop for auto mode"""
        while True:
            try:
                await self.process_auto_users()
            except Exception as e:
                print(f"[AUTO MODE ERROR] {e}")

            await asyncio.sleep(self.interval)

    async def process_auto_users(self):
        """Send signals to all users with Auto Mode ON"""

        users = self.user_storage.get_auto_users()

        if not users:
            return

        pair = self.pair_detector.auto()
        signal = self.signal_engine.generate_signal(pair)

        sender = SignalSender(self.bot)

        for user_id in users:
            await sender.send_signal(
                user_id=user_id,
                signal=signal,
                pair=pair
            )

            print(f"[AUTO] Sent signal to {user_id} at {datetime.utcnow()}")
