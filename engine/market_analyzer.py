import aiohttp
import numpy as np
import time


class MarketAnalyzer:
    """
    Market Analyzer fetches real market data and calculates:
    - Trend Strength (EMA + Slope)
    - Volatility (ATR)
    - Momentum (RSI)
    """

    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3/klines"
        self.default_interval = "1m"
        self.cache = {}  # prevents rate-limit, stores last data briefly
        self.cache_expiry = 5  # seconds

    async def fetch_candles(self, symbol: str, limit: int = 50):
        """
        Fetch live candles from Binance API.
        """
        now = time.time()

        # ─── Cached data prevention ──────────────────────────
        if symbol in self.cache:
            saved, timestamp = self.cache[symbol]
            if now - timestamp <= self.cache_expiry:
                return saved

        params = {
            "symbol": symbol.upper(),
            "interval": self.default_interval,
            "limit": limit
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as r:
                if r.status != 200:
                    return None

                data = await r.json()
                closes = [float(i[4]) for i in data]   # closing prices
                highs = [float(i[2]) for i in data]    # high prices
                lows = [float(i[3]) for i in data]     # low prices

                self.cache[symbol] = ((closes, highs, lows), now)
                return closes, highs, lows

    # ───────────────────────────────────────────────────────────
    # INDICATORS
    # ───────────────────────────────────────────────────────────

    def rsi(self, closes, period: int = 14):
        deltas = np.diff(closes)
        seed = deltas[:period]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period if any(seed < 0) else 0
        rs = up / down if down != 0 else 0
        rsi_list = np.zeros_like(closes)
        rsi_list[:period] = 50

        for i in range(period, len(closes)):
            delta = deltas[i - 1]
            up_val = max(delta, 0)
            down_val = -min(delta, 0)
            up = (up * (period - 1) + up_val) / period
            down = (down * (period - 1) + down_val) / period if down != 0 else 0
            rs = up / down if down != 0 else 0
            rsi_list[i] = 100 - (100 / (1 + rs))
        return rsi_list[-1]

    def atr(self, highs, lows, closes, period: int = 14):
        trs = []
        for i in range(1, len(closes)):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i - 1])
            low_close = abs(lows[i] - closes[i - 1])
            tr = max(high_low, high_close, low_close)
            trs.append(tr)

        if len(trs) < period:
            return np.mean(trs)
        return np.mean(trs[-period:])

    def trend_strength(self, closes):
        """
        Measures trend strength using EMA slope.
        """
        ema_period = 20
        alpha = 2 / (ema_period + 1)

        ema = closes[0]
        ema_values = []
        for price in closes:
            ema = (price - ema) * alpha + ema
            ema_values.append(ema)

        # Trend slope
        slope = ema_values[-1] - ema_values[-5]

        return slope

    # ───────────────────────────────────────────────────────────
    # MAIN ANALYSIS
    # ───────────────────────────────────────────────────────────

    async def analyze(self, symbol: str):
        """
        Analyze market for a specific symbol and return real metrics.
        """
        data = await self.fetch_candles(symbol)
        if data is None:
            return None

        closes, highs, lows = data

        if len(closes) < 20:
            return None

        rsi_value = self.rsi(closes)
        atr_val = self.atr(highs, lows, closes)
        trend = self.trend_strength(closes)

        return {
            "rsi": round(rsi_value, 2),
            "atr": round(atr_val, 5),
            "trend": round(trend, 5),
            "last_price": closes[-1]
          }
