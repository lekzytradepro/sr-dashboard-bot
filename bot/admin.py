# bot/admin.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.utils import is_admin, broadcast_message
from bot.data_feed import get_active_assets

router = Router()


@router.message(Command("admin"))
async def admin_panel(msg: Message):
    """Admin command menu"""
    if not is_admin(msg.from_user.id):
        return await msg.answer("❌ You are not authorized to use admin commands.")

    txt = (
        "<b>🔐 Admin Control Panel</b>\n\n"
        "Available commands:\n"
        "• /broadcast - Send message to all subscribers\n"
        "• /assets - Show active trading assets\n"
    )
    await msg.answer(txt)


@router.message(Command("broadcast"))
async def admin_broadcast(msg: Message):
    """Send a message to all users"""
    if not is_admin(msg.from_user.id):
        return await msg.answer("❌ You are not authorized.")

    parts = msg.text.split(" ", 1)
    if len(parts) < 2:
        return await msg.answer("ℹ️ Usage: <code>/broadcast Your message here</code>")

    text_to_send = parts[1]
    await msg.answer("📨 Broadcasting message...")

    count = await broadcast_message(text_to_send)
    await msg.answer(f"✅ Message sent to <b>{count}</b> users.")


@router.message(Command("assets"))
async def active_assets(msg: Message):
    """List tracked assets"""
    if not is_admin(msg.from_user.id):
        return await msg.answer("❌ Not authorized.")

    assets = get_active_assets()

    if not assets:
        return await msg.answer("No active assets found.")

    formatted = "\n".join([f"• {a}" for a in assets])
    await msg.answer(f"📊 <b>Active Assets</b>:\n{formatted}")
