import os
from datetime import timezone

# ========== BOT SECRET SETTINGS ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
ADMIN_IDS = [ADMIN_ID]  # Add this line - creates a list with your single admin ID

# ========== TIME SETTINGS ==========
# We ALWAYS use UTC for server stability
BOT_TIMEZONE = timezone.utc

# ========== SIGNAL ENGINE SETTINGS ==========
DEFAULT_PAIRS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "XAUUSD",
]

DEFAULT_TIMEFRAME = "1MIN"   # can be 1MIN, 5MIN, 15MIN...
MIN_CONFIDENCE = 70          # minimum confidence to send signals

# ========== PRE-ENTRY SETTINGS ==========
SEND_PRE_ENTRY = True        # send pre-entry notification?
PRE_ENTRY_DELAY = 20         # seconds before main entry

# ========== BOT LOOP SETTINGS ==========
CHECK_INTERVAL = 30          # seconds between pair checks
