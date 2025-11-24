from datetime import datetime

def generate_reason(direction, strategy, indicators):
    now = datetime.now().strftime("%H:%M")

    # Direction text
    dir_text = "UP" if direction == "BUY" else "DOWN"

    # Strategy text
    strat_text = ""
    if strategy == "breakout":
        strat_text = "Price broke a structure level with strong pressure."
    elif strategy == "reversal":
        strat_text = "Market reversed from a key area with momentum."
    elif strategy == "trend-follow":
        strat_text = "Trend direction confirmed with stable continuation."
    else:
        strat_text = "Optimal market conditions detected."

    # Indicator notes
    ind_notes = []
    if indicators.get("rsi") == "oversold":
        ind_notes.append("RSI shows oversold conditions → bullish expectation.")
    if indicators.get("rsi") == "overbought":
        ind_notes.append("RSI shows overbought conditions → bearish expectation.")
    if indicators.get("macd") == "bullish":
        ind_notes.append("MACD crossover confirms bullish movement.")
    if indicators.get("macd") == "bearish":
        ind_notes.append("MACD crossover confirms bearish pressure.")
    if indicators.get("support"):
        ind_notes.append("Price reacted at support zone.")
    if indicators.get("resistance"):
        ind_notes.append("Price reacted at resistance zone.")
    if indicators.get("momentum") == "strong":
        ind_notes.append("Strong momentum detected in candle pattern.")
    if indicators.get("momentum") == "weak":
        ind_notes.append("Market shows weakening momentum.")

    indicator_text = "\n".join(ind_notes)

    # Final message
    msg = f"""
📊 *Signal Breakdown*
⏰ Entry Time: {now}
📈 Direction: {dir_text}

✨ *Why this signal?*
{strat_text}

🔍 *Indicator Analysis*
{indicator_text if indicator_text else "Indicators align for optimal entry."}

⚡ Execute with proper risk management.
"""

    return msg
