# bot/handlers.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.signal_sender import SignalSender
from engine.pair_detector import PairDetector
from engine.signal_storage import SignalEngine
from aiogram import Bot
from bot.keyboards import main_menu
from storage.user_storage import UserStorage
from aiogram.types import CallbackQuery

router = Router()

# Initialize engine + pair module
pair_detector = PairDetector()
signal_engine = SignalEngine()


async def send_signal_flow(message: Message, bot: Bot, pair: str):
    """ Generates a signal + sends it to user """
    
    # detect pair if needed
    if pair == "AUTO":
        pair = pair_detector.auto()
    
    # generate signal
    signal = signal_engine.generate_signal(pair)

    
   sender = SignalSender(bot, user_db=user_storage)
await sender.send_signal(
    user_id=message.from_user.id,
    signal=signal,
    pair=pair
) 


# ===========================
#       COMMAND HANDLERS
# ===========================

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Welcome! Tap *Get Signal* to begin.", parse_mode="Markdown")


@router.message(F.text == "📡 Get Signal")
async def manual_signal(message: Message, bot: Bot):
    await send_signal_flow(message, bot, pair="AUTO")


@router.message(F.text == "🔁 Refresh")
async def refresh_signal(message: Message, bot: Bot):
    await send_signal_flow(message, bot, pair="AUTO")


@router.message(Command("signal"))
async def signal_direct(message: Message, bot: Bot):
    await send_signal_flow(message, bot, pair="AUTO")
