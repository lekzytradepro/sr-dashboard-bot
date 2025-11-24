from aiogram import Router, types
from aiogram.filters import Command
from .keyboards import main_menu_keyboard
import asyncio
from datetime import datetime, timedelta
from ai.engine import QuantumAIEngine
from core.utils import format_signal_message, get_current_pair_time

router = Router()
SCAN_INTERVAL = 180  # 3 minutes


@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer(
        "👋 <b>Quantum Matrix AI Bot Activated!</b>\n\n"
        "I will automatically scan multiple forex pairs every 3 minutes.\n"
        "Whenever a strong BUY or SELL setup appears, I'll send it immediately.\n\n"
        "Use the menu below 👇",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.message(lambda m: m.text == "📈 Manual Signal")
async def manual_signal(msg: types.Message):
    engine = QuantumAIEngine()
    pair = engine.get_random_pair()

    result = engine.get_signal(pair)

    if result["recommendation"] == "NEUTRAL":
        await msg.answer("⚪ Market is not safe right now. Try again shortly.")
        return

    expected = (datetime.utcnow() + timedelta(minutes=3)).strftime("%H:%M:%S")

    message = format_signal_message(
        pair=pair,
        recommendation=result["recommendation"],
        confidence=result["confidence"],
        current_time=get_current_pair_time(),
        expected_entry=expected,
        indicators=result["indicators"]
    )

    await msg.answer(message, parse_mode="Markdown")


async def auto_scanner(bot, pairs):
    engine = QuantumAIEngine()
    await asyncio.sleep(3)

    while True:
        try:
            for pair in pairs:
                now = datetime.utcnow()
                expected_entry = now + timedelta(minutes=3)

                result = engine.get_signal(pair)

                if result and result["recommendation"] != "NEUTRAL":
                    msg = format_signal_message(
                        pair=pair,
                        recommendation=result["recommendation"],
                        confidence=result["confidence"],
                        current_time=get_current_pair_time(),
                        expected_entry=expected_entry.strftime("%H:%M:%S"),
                        indicators=result["indicators"]
                    )

                    await bot.send_message(
                        chat_id="-100XXXXXXXXXXXX",  # your channel ID
                        text=msg,
                        parse_mode="Markdown"
                    )

            await asyncio.sleep(SCAN_INTERVAL)

        except Exception as e:
            print("Scanner error:", e)
            await asyncio.sleep(10)
