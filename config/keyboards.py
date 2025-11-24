from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# =========================
# MAIN MENU KEYBOARD
# =========================
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📈 Manual Signal")],
            [KeyboardButton(text="⚙️ Settings")]
        ],
        resize_keyboard=True
    )


# =========================
# SETTINGS MENU
# =========================
def settings_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔔 Toggle Pre-Entry")],
            [KeyboardButton(text="🎯 Set Min Confidence")],
            [KeyboardButton(text="🌍 Change Timezone")],
            [KeyboardButton(text="⬅️ Back")]
        ],
        resize_keyboard=True
    )


# =========================
# INLINE PAIR SELECTOR
# =========================
def pair_selector():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="EUR/USD", callback_data="pair_EURUSD"),
                InlineKeyboardButton(text="GBP/USD", callback_data="pair_GBPUSD")
            ],
            [
                InlineKeyboardButton(text="XAU/USD", callback_data="pair_XAUUSD"),
                InlineKeyboardButton(text="USD/JPY", callback_data="pair_USDJPY")
            ],
            [
                InlineKeyboardButton(text="AUD/USD", callback_data="pair_AUDUSD")
            ]
        ]
    )


# =========================
# BACK BUTTON (INLINE)
# =========================
def back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu")]
        ]
    )
