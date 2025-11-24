from datetime import datetime

class AnalysisBuilder:
    @staticmethod
    def build_reasoning(indicator_data: dict) -> str:
        reasoning = []

        # Trend direction
        if indicator_data.get("trend") == "uptrend":
            reasoning.append("The overall trend is bullish and forming higher lows.")
        elif indicator_data.get("trend") == "downtrend":
            reasoning.append("The market is in a bearish trend with consistent lower highs.")
        else:
            reasoning.append("The market is ranging without a clear trend.")

        # Support / Resistance reaction
        if indicator_data.get("near_support"):
            reasoning.append("Price reacted strongly from a support zone.")
        if indicator_data.get("near_resistance"):
            reasoning.append("Price rejected a key resistance level.")

        # RSI condition
        rsi = indicator_data.get("rsi")
        if rsi is not None:
            if rsi < 30:
                reasoning.append("RSI indicates oversold conditions, favoring an upward reversal.")
            elif rsi > 70:
                reasoning.append("RSI indicates overbought conditions, favoring a downward correction.")

        # Momentum strength
        if indicator_data.get("momentum") == "strong":
            reasoning.append("Momentum aligns strongly with the signal direction.")
        else:
            reasoning.append("Momentum is weak, but other indicators support the setup.")

        return " ".join(reasoning)

    @staticmethod
    def final_message(pair, direction, entry_time, confidence, reasoning):
        direction_emoji = "⬆️ UP" if direction == "BUY" else "⬇️ DOWN"

        return (
            f"📌 *AI Smart Signal*\n"
            f"Pair: *{pair}*\n"
            f"Direction: *{direction_emoji}*\n"
            f"Entry Time: *{entry_time}*\n"
            f"Confidence: *{confidence}%*\n\n"
            f"🧠 *Reasoning:*\n{reasoning}"
        )
