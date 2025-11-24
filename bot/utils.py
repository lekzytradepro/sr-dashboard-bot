# utils.py

from datetime import datetime

def format_signal_message(result: dict) -> str:
    """
    Format the AI signal output into a clean message.
    """

    direction_icon = "⬆️ BUY" if result["direction"] == "BUY" else "⬇️ SELL"

    confidence = result["confidence"]
    if confidence >= 80:
        conf_type = "🟢 Strong"
    elif confidence >= 60:
        conf_type = "🟡 Medium"
    else:
        conf_type = "🔴 Weak"

    return (
        "🔮 <b>AI MARKET SIGNAL</b>\n\n"
        f"📌 <b>Pair:</b> {result['pair']}\n"
        f"🧭 <b>Direction:</b> {direction_icon}\n"
        f"📊 <b>Confidence:</b> {confidence}% ({conf_type})\n\n"
        f"📈 <b>Indicator Breakdown:</b>\n"
        f"• RSI: {result['rsi']}\n"
        f"• EMA Trend: {result['ema_trend']}\n"
        f"• MACD: {result['macd']}\n"
        f"• ADX: {result['adx']}\n\n"
        f"📝 <b>Analysis:</b>\n"
        f"{result['reason']}\n\n"
        f"⏱ <b>Generated:</b> {current_time()}\n"
    )


def current_time():
    return datetime.now().strftime("%H:%M:%S")
