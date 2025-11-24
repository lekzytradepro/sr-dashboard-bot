# bot/auth.py

from bot.utils import user_db, is_admin
from aiogram.types import Message


async def ensure_user_registered(msg: Message):
    """
    Ensures the user exists in the database.
    If not, create an entry for them.
    """
    user_id = msg.from_user.id
    full_name = msg.from_user.full_name

    # Register if user is new
    if not user_db.user_exists(user_id):
        user_db.add_user(user_id, full_name)
        await msg.answer(
            f"👋 Welcome <b>{full_name}</b>!\n"
            "Your account has been created successfully. 🎉"
        )


async def ensure_subscription_active(msg: Message):
    """
    Verifies if a user is active (paid or allowed).
    Admins automatically pass.
    """
    user_id = msg.from_user.id

    if is_admin(user_id):
        return True  # Admin passes all restrictions

    if not user_db.is_user_active(user_id):
        await msg.answer(
            "⛔ Your subscription is inactive.\n\n"
            "Please contact support to activate your access."
        )
        return False

    return True
