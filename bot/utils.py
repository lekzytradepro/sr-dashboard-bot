# bot/utils.py
import datetime

def current_time():
    """Returns current time in HH:MM format."""
    return datetime.datetime.now().strftime("%H:%M")

def entry_time_after(minutes=1):
    """Returns future entry time after X minutes in HH:MM format."""
    t = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    return t.strftime("%H:%M")

def arrow(direction):
    """Return UP/DOWN icons."""
    return "⬆️" if direction == "UP" else "⬇️"

def clean_asset_name(asset: str):
    """Format names like 'EURUSD_otc' → 'EUR/USD'."""
    asset = asset.replace("_", "").replace("otc", "")
    return f"{asset[0:3]}/{asset[3:6]}"

def format_signal_message(asset, direction, strength, reason):
    """
    Build final signal message with:
    - asset
    - direction + arrow
    - time
    - entry time
    - strength
    - reason
    """

    return (
        f"📊 *AUTO SIGNAL*\n"
        f"────────────────────\n"
        f"🕒 Time: *{current_time()}*\n"
        f"⌛ Entry Time: *{entry_time_after(1)}*\n"
        f"💹 Asset: *{clean_asset_name(asset)}*\n"
        f"📈 Direction: *{direction} {arrow(direction)}*\n"
        f"🔥 Strength: *{strength}%*\n\n"
        f"📝 Reason:\n"
        f"{reason}"
    )
