# bot/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    """
    Main menu shown after /start.
    """
    kb = [
        [KeyboardButton(text="📈 Manual Signal")],
        [KeyboardButton(text="⚙️ Settings")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )


def confirm_activation_kb():
    """
    Inline keyboard for subscription activation confirmation.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Activate Subscription", callback_data="activate_sub")
            ]
        ]
    )


def admin_menu():
    """
    Additional inline menu for admins.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Force Send Signal", callback_data="admin_send_signal")
            ],
            [
                InlineKeyboardButton(text="👥 View Users", callback_data="admin_users")
            ]
        ]
    )
