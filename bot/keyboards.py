# bot/keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📡 Get Signal", callback_data="get_signal")
        ],
        [
            InlineKeyboardButton(text="🚀 Start Auto Mode", callback_data="auto_on")
        ],
        [
            InlineKeyboardButton(text="🛑 Stop Auto Mode", callback_data="auto_off")
        ]
    ])
