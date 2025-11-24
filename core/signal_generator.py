import datetime
from typing import Dict, Any

class SignalGenerator:
    def __init__(self, ai_engine, utils):
        self.ai_engine = ai_engine
        self.utils = utils

    def generate(self, pair: str, timeframe: str = "1m") -> Dict[str, Any]:
        """
        Generate a full signal package including:
        - direction (BUY/SELL)
        - analysis reasons
        - entry time
        - expected next entry window
        """

        # 1. fetch market data
        data = self.utils.fetch_market_data(pair, timeframe)
        if data is None:
            return {
                "status": "error",
                "message": "Failed to fetch market data."
            }

        # 2. get engine prediction
        engine_output = self.ai_engine.predict(data)

        direction = engine_output.get("direction", "neutral")
        confidence = engine_output.get("confidence", 0)

        # 3. generate entry times
        now = datetime.datetime.utcnow()
        entry_time = now.strftime("%H:%M UTC")
        next_entry = (now + datetime.timedelta(minutes=1)).strftime("%H:%M UTC")

        # 4. generate analysis
        analysis_reason = self._generate_reason(direction, data)

        return {
            "status": "success",
            "pair": pair,
            "timeframe": timeframe,
            "direction": direction.upper(),
            "confidence": confidence,
            "entry_time": entry_time,
            "next_entry": next_entry,
            "analysis": analysis_reason
        }

    def _generate_reason(self, direction: str, data: Dict[str, Any]) -> str:
        """
        Convert engine direction into a human-readable explanation
        """

        close = data["close"]
        prev = data["prev_close"]

        if direction == "buy":
            if close > prev:
                return (
                    "The market is showing bullish momentum. "
                    "Price pushed upward and stayed above the previous candle — "
                    "indicating a strong UP continuation."
                )
            return (
                "Engine detected potential upward pressure even though current "
                "candle is not strongly bullish."
            )

        if direction == "sell":
            if close < prev:
                return (
                    "The market is pushing downward with momentum. "
                    "Price stayed below the previous candle — a sign of continued DOWN movement."
                )
            return (
                "Engine detected selling pressure despite the candle not fully confirming it."
            )

        return "No strong signal. Market is moving sideways with low strength."
