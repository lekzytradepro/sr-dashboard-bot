# bot/utils.py
import datetime
from aiogram import Bot
from config.settings import ADMIN_IDS


# ------------------------- #
#  TIME HELPERS
# ------------------------- #

def current_time():
    """Returns current time in HH:MM format."""
    return datetime.datetime.now().strftime("%H:%M")


def entry_time_after(minutes=1):
    """Returns future entry time after X minutes in HH:MM format."""
    t = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    return t.strftime("%H:%M")


# ------------------------- #
#  SIGNAL FORMAT HELPERS
# ------------------------- #

def arrow(direction):
    """Return UP/DOWN icons."""
    return "📈" if direction == "UP" else "📉"


def clean_asset_name(asset: str):
    """Format pairs like 'EURUSD_otc' -> 'EUR/USD'."""
    asset = asset.replace("_", "").replace("otc", "")
    return f"{asset[0:3]}/{asset[3:6]}"


def format_signal_message(asset, direction, strength, reason):
    """
    Build final signal message with:
    - asset
    - direction + arrow
    - time
    - entry time
    - strength
    - reason
    """
    return (
        f"📊 *AUTO SIGNAL*\n"
        f"──────────────────────\n"
        f"🕒 Time: *{current_time()}*\n"
        f"⏳ Entry Time: *{entry_time_after(1)}*\n"
        f"💹 Asset: *{clean_asset_name(asset)}*\n"
        f"➡️ Direction: *{direction} {arrow(direction)}*\n"
        f"🔥 Strength: *{strength}%*\n\n"
        f"📝 Reason:\n"
        f"{reason}"
    )


# ------------------------- #
#  ADMIN UTILITIES
# ------------------------- #

def is_admin(user_id: int) -> bool:
    """Check if user ID belongs to admin."""
    return user_id in ADMIN_IDS


async def broadcast_message(bot: Bot, users: list[int], text: str):
    """Send a message to multiple users safely."""
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=text)
        except Exception:
            continue


def log(msg: str):
    """Simple console logger."""
    print(f"[BOT] {msg}")
