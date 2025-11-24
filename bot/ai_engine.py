from .analysis_builder import AnalysisBuilder

class SignalGenerator:
    """
    Generates trading signals + reasons from indicator data.
    Produces final text message for the bot.
    """

    @staticmethod
    def generate(pair: str, indicator_data: dict) -> str:
        """
        indicator_data expected structure:
        {
            "bounce": True/False,
            "momentum": "strong"/"weak",
            "candle_strength": "strong"/"weak",
            "level": "support"/"resistance",
            "direction": "BUY" or "SELL",
            "confidence": float between 0–100
        }
        """

        direction = indicator_data.get("direction", "BUY")
        confidence = indicator_data.get("confidence", 75)

        # Build human-readable explanations
        reason_data = {
            "bounce": indicator_data.get("bounce", False),
            "momentum": indicator_data.get("momentum", ""),
            "candle_strength": indicator_data.get("candle_strength", ""),
            "level": indicator_data.get("level", "")
        }

        # Build final message
        message = AnalysisBuilder.build_signal_message(
            pair=pair,
            direction=direction,
            confidence=confidence,
            reason_data=reason_data
        )

        return message
