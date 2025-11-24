from datetime import datetime

class AnalysisBuilder:
    """
    Builds human-readable analysis text for trading signals.
    Adds reasons, timing, direction explanation, and context.
    """

    @staticmethod
    def format_time():
        """Returns current time formatted for signal output."""
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def direction_arrow(direction: str) -> str:
        return "⬆️ UP" if direction.upper() == "BUY" else "⬇️ DOWN"

    @staticmethod
    def build_reason(reason_data: dict) -> str:
        """
        Converts raw AI-engine reasons into readable explanations.
        Expected keys:
         - bounce: True/False
         - momentum: "strong" / "weak"
         - level: "support" / "resistance"
         - candle_strength: "strong" / "weak"
        """

        parts = []

        if reason_data.get("bounce"):
            lvl = reason_data.get("level", "support/resistance")
            parts.append(f"The price bounced off the {lvl} level.")

        if reason_data.get("momentum") == "strong":
            parts.append("Market momentum is strong in this direction.")

        if reason_data.get("candle_strength") == "strong":
            parts.append("Recent candles confirm the push.")

        if not parts:
            parts.append("Market conditions support this entry.")

        return " ".join(parts)

    @staticmethod
    def build_signal_message(pair: str, direction: str, confidence: float, reason_data: dict) -> str:
        """
        Creates the final message the bot sends to the user.
        """

        entry_time = AnalysisBuilder.format_time()
        arrow = AnalysisBuilder.direction_arrow(direction)
        reasons = AnalysisBuilder.build_reason(reason_data)

        return (
            f"📌 *AI Smart Signal*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💹 *Pair:* {pair}\n"
            f"🕒 *Entry Time:* {entry_time}\n"
            f"📈 *Direction:* {arrow}\n"
            f"🔰 *Confidence:* {confidence}%\n\n"
            f"🧠 *Reasoning:*\n"
            f"{reasons}"
        )
