from datetime import datetime
from bot.core.reason_generator import ReasonGenerator


class SignalFormatter:
    """
    Formats the final trading signal into a beautiful message
    that goes to the user or Telegram channel.
    """

    @staticmethod
    def format_time():
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def direction_arrow(direction: str) -> str:
        return "📈 BUY" if direction.upper() == "BUY" else "📉 SELL"

    @staticmethod
    def build_final_message(pair: str, direction: str, confidence: float, reason_data: dict) -> str:
        """
        Combines:
        - formatted time
        - direction arrow
        - human-readable reasons
        - confidence percentage
        into a single message.
        """

        time_str = SignalFormatter.format_time()
        arrow = SignalFormatter.direction_arrow(direction)
        reasons = ReasonGenerator.build(reason_data)

        return (
            f"🤖 *AI Smart Signal*\n"
            f"────────────────────\n"
            f"🔹 *Pair:* {pair}\n"
            f"🔹 *Direction:* {arrow}\n"
            f"🔹 *Confidence:* {confidence:.1f}%\n"
            f"🔹 *Time:* {time_str}\n\n"
            f"🧠 *Why this signal?*\n"
            f"{reasons}\n"
        )
