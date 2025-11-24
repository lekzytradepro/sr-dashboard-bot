# bot/keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_keyboard():
    """
    Main menu keyboard.
    """
    kb = [
        [InlineKeyboardButton(text="📊 Signals", callback_data="signals_menu")],
        [InlineKeyboardButton(text="⚙️ Settings", callback_data="settings_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def signal_pairs_keyboard():
    """
    List of supported trading pairs.
    You can add or remove pairs later.
    """
    pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

    kb = [[InlineKeyboardButton(text=p, callback_data=f"pair_{p}")] for p in pairs]

    kb.append([InlineKeyboardButton(text="⬅️ Back", callback_data="back_menu")])

    return InlineKeyboardMarkup(inline_keyboard=kb)


def admin_keyboard():
    """
    Admin-only options.
    """
    kb = [
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="⚡ Manual Signal", callback_data="admin_signal")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
