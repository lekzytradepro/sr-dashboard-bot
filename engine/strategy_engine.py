class StrategyEngine:
    """
    Generates BUY / SELL / NEUTRAL direction based on
    real technical analysis from MarketAnalyzer.
    """

    def __init__(self):
        pass

    def generate_direction(self, market):
        """
        Accepts market data:
        {
            "rsi": float,
            "trend": float,
            "atr": float,
            "candle_dir": "UP" / "DOWN",
            "volatility": float
        }

        Returns:
            "BUY", "SELL", or "NEUTRAL"
        """

        rsi = market["rsi"]
        trend = market["trend"]
        atr = market["atr"]
        candle = market["candle_dir"]
        vol = market["volatility"]

        # Reject dead markets (no volatility)
        if atr == 0 or vol < 0.1:
            return "NEUTRAL"

        # Reject unstable RSI extremes
        if rsi < 20 or rsi > 80:
            return "NEUTRAL"

        # RSI BUY zone
        if 35 <= rsi <= 55 and trend > 0 and candle == "UP":
            return "BUY"

        # RSI SELL zone
        if 45 <= rsi <= 65 and trend < 0 and candle == "DOWN":
            return "SELL"

        # Trend-only conditions
        if trend > 0.05 and candle == "UP":
            return "BUY"

        if trend < -0.05 and candle == "DOWN":
            return "SELL"

        # Default
        return "NEUTRAL"
