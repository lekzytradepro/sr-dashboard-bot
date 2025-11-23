# core/signal_dispatcher.py

import asyncio
from datetime import datetime
from engine.asset_detector import AssetDetector
from core.ai_signal_engine import AISignalEngine
from storage.user_storage import UserStorage
from aiogram import Bot

class SignalDispatcher:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.detector = AssetDetector()
        self.ai_engine = AISignalEngine()
        self.user_db = UserStorage()

    async def start_auto_signals(self):
        """
        Auto signal loop – runs forever and sends new signals when ready.
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

            # Delay before next signal
            await asyncio.sleep(60)

    async def send_to_all_users(self, signal):
        """Send signal to all active subscribers"""
        users = self.user_db.get_all_active_users()

        if not users:
            return

        msg = self.format_signal(signal)

        for user in users:
            try:
                await self.bot.send_message(chat_id=user, text=msg, parse_mode="HTML")
            except:
                continue

    def format_signal(self, s):
        """
        Formats signal message in a clean professional layout
        """
        return f"""
📡 <b>AI Premium Market Signal</b>
────────────────────

<b>Asset:</b> {s['asset']}
<b>Direction:</b> {s['direction']}
<b>Confidence:</b> {s['confidence']}%

<b>Indicators:</b>
• RSI: {s['rsi']}
• MACD: {s['macd']}
• Signal Line: {s['signal_line']}
• EMA20: {s['ema20']}
• EMA50: {s['ema50']}

<b>Generated:</b> {s['timestamp']}

⚠️ Always combine with your price action.
        """
