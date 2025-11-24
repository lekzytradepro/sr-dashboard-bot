import asyncio
from engine.market_analyzer import MarketAnalyzer


class PairDetector:
    """
    Detects the best trading pair by scanning multiple symbols
    and selecting the one with stable trend + healthy volatility.
    """

    def __init__(self):
        self.analyzer = MarketAnalyzer()

        # REAL crypto pairs (Binance)
        self.symbols = [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "SOLUSDT",
            "XRPUSDT",
            "DOGEUSDT",
            "ADAUSDT",
            "TRXUSDT"
        ]

    async def score_pair(self, symbol):
        """
        Scores each pair based on trend strength, ATR volatility,
        and RSI stability. Higher score = better market.
        """

        market = await self.analyzer.analyze(symbol)
        if market is None:
            return None

        rsi = market["rsi"]
        atr = market["atr"]
        trend = market["trend"]

        score = 0

        # RSI scoring
        if 45 <= rsi <= 55:
            score += 3  # perfect neutral zone
        elif 35 <= rsi <= 65:
            score += 2
        else:
            score -= 2  # overbought/oversold → risky

        # ATR scoring (volatility)
        if atr > 0:
            score += 1

        # Trend scoring
        if abs(trend) > 0.05:
            score += 2  # healthy trend
        elif abs(trend) > 0.02:
            score += 1  # weak but valid trend

        return {
            "symbol": symbol,
            "score": score,
            "data": market
        }

    async def get_best_pair(self):
        """
        Scans all symbols and returns the one with
        the highest REAL-MARKET score.
        """

        tasks = [self.score_pair(sym) for sym in self.symbols]
        results = await asyncio.gather(*tasks)

        # remove empty responses
        valid = [r for r in results if r is not None]

        if not valid:
            return None

        best = max(valid, key=lambda x: x["score"])

        return best["symbol"]
