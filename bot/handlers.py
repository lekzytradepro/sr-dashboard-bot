# bot/handlers.py

from aiogram import Router, types
from aiogram.filters import Command
from storage.user_storage import UserStorage
from bot.keyboards import main_menu
from core.signal_dispatcher import SignalDispatcher

router = Router()
user_db = UserStorage()


@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    user_id = msg.from_user.id
    user_db.add_user(user_id)

    await msg.answer(
        "👋 <b>Welcome to SR Dashboard AI Bot!</b>\n\n"
        "Your account is now activated.\n"
        "You will start receiving AI auto-signals automatically.\n\n"
        "Use the menu below to request manual signals or settings 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def help_cmd(msg: types.Message):
    await msg.answer(
        "<b>📘 HELP MENU</b>\n\n"
        "• /start – Activate bot\n"
        "• Manual Signal – Get instant signal\n"
        "• Auto Mode – Signals will be sent automatically\n\n"
        "If you need new features, just tell me!",
        parse_mode="HTML"
    )


@router.message(lambda m: m.text == "📈 Manual Signal")
async def manual_signal(msg: types.Message):
    """User requests a manual signal instantly."""
    user_id = msg.from_user.id

    dispatcher = SignalDispatcher(bot=msg.bot)
    asset = dispatcher.detector.get_best_pair()

    if asset is None:
        await msg.answer("⚠️ No tradeable asset available right now. Try again later.")
        return

    signal = dispatcher.ai_engine.generate_signal(asset)

    if signal["direction"] == "NEUTRAL":
        await msg.answer("⚪ Market not safe for entry right now.")
        return

    formatted = dispatcher.format_signal(signal)
    await msg.answer(formatted, parse_mode="HTML")


@router.message(lambda m: m.text == "⚙️ Settings")
async def settings_cmd(msg: types.Message):
    await msg.answer(
        "⚙️ <b>Settings Page</b>\n\n"
        "More settings will be added soon.",
        parse_mode="HTML"
    )
