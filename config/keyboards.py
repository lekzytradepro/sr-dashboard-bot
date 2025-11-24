from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📈 Manual Signal")],
            [KeyboardButton(text="⚙️ Settings")],
        ],
        resize_keyboard=True
    )


def settings_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔔 Toggle Pre-Entry")],
            [KeyboardButton(text="🎯 Minimum Confidence")],
            [KeyboardButton(text="⬅️ Back to Menu")],
        ],
        resize_keyboard=True
    )
