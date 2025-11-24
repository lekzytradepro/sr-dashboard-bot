# bot/ai_engine.py
import numpy as np


class AIEngine:
    def __init__(self):
        pass

    def rsi(self, closes, period=14):
        """Calculate RSI."""
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def ema(self, data, period):
        """Calculate EMA."""
        return np.mean(data[-period:])

    def macd(self, closes):
        """Calculate a simple MACD."""
        ema12 = self.ema(closes, 12)
        ema26 = self.ema(closes, 26)
        return ema12 - ema26

    def adx(self, highs, lows, closes, period=14):
        """Basic ADX approximation."""
        tr = np.maximum(highs[1:], closes[:-1]) - np.minimum(lows[1:], closes[:-1])
        tr = np.where(tr == 0, 1, tr)

        dx = (np.abs(highs[1:] - lows[1:]) / tr) * 100
        return np.mean(dx[-period:])

    def generate_signal(self, candles):
        """
        Main signal generator.
        candles = dict with keys: open, high, low, close
        Each contains list/array of prices.
        """
        closes = np.array(candles["close"])
        highs = np.array(candles["high"])
        lows = np.array(candles["low"])

        # Indicators
        rsi_val = self.rsi(closes)
        macd_val = self.macd(closes)
        adx_val = self.adx(highs, lows, closes)

        # Decision logic
        signal = "NEUTRAL"
        confidence = 0

        if rsi_val < 30 and macd_val > 0 and adx_val > 20:
            signal = "BUY"
            confidence = 70 + min(30, int(adx_val))

        elif rsi_val > 70 and macd_val < 0 and adx_val > 20:
            signal = "SELL"
            confidence = 70 + min(30, int(adx_val))

        else:
            signal = "NEUTRAL"
            confidence = 45

        return {
            "signal": signal,
            "rsi": round(rsi_val, 2),
            "macd": round(macd_val, 4),
            "adx": round(adx_val, 2),
            "confidence": confidence
  }
