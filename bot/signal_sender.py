# bot/signal_sender.py

from aiogram import Bot
from datetime import datetime
from storage.signal_storage import SignalStorage

class SignalSender:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.storage = SignalStorage()

    async def send_signal(self, user_id: int, signal: str, pair: str):
        """
        Sends a formatted signal to the user.
        """

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        message_text = (
            f"📡 **SR DASHBOARD PRO SIGNAL**\n"
            f"──────────────────────────────\n"
            f"💹 **Pair:** {pair}\n"
            f"📊 **Decision:** {signal}\n"
            f"⏰ **Time:** {timestamp}\n"
        )

        # save to storage
        self.storage.save_signal({
            "pair": pair,
            "signal": signal,
            "time": timestamp
        })

        await self.bot.send_message(
            chat_id=user_id,
            text=message_text,
            parse_mode="Markdown"
        )
