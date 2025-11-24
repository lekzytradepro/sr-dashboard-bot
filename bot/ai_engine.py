# ai_engine.py

class AIEngine:
    def __init__(self):
        pass

    def generate_signal(self, candles):
        """
        candles = list of OHLC data.
        We use the last 2–3 candles for indicators.
        """
        last = candles[-1]
        prev = candles[-2]

        close_prices = [c['close'] for c in candles]

        rsi = self.calculate_rsi(close_prices)
        ema_fast = self.calculate_ema(close_prices, period=5)
        ema_slow = self.calculate_ema(close_prices, period=13)
        macd = ema_fast - ema_slow
        adx = self.fake_adx(close_prices)

        # Direction logic
        if rsi < 30 or ema_fast > ema_slow or macd > 0:
            direction = "BUY"
        else:
            direction = "SELL"

        # Confidence
        confidence = self.calculate_confidence(rsi, ema_fast, ema_slow, macd, adx, direction)

        # Reason generator
        reason = self.generate_reason(rsi, ema_fast, ema_slow, macd, adx, direction)

        return {
            "pair": "AUTO-PAIR",
            "direction": direction,
            "confidence": confidence,
            "rsi": round(rsi, 2),
            "ema_trend": "UPTREND" if ema_fast > ema_slow else "DOWNTREND",
            "macd": round(macd, 4),
            "adx": round(adx, 2),
            "reason": reason
        }

    # ------------------------------
    # INDICATORS
    # ------------------------------

    def calculate_rsi(self, closes, period=14):
        if len(closes) < period + 1:
            return 50
        gains = []
        losses = []
        for i in range(1, period + 1):
            diff = closes[-i] - closes[-i-1]
            if diff > 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))
        avg_gain = sum(gains) / period if gains else 0.01
        avg_loss = sum(losses) / period if losses else 0.01
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def calculate_ema(self, closes, period):
        if len(closes) < period:
            return closes[-1]
        k = 2 / (period + 1)
        ema = closes[0]
        for price in closes:
            ema = price * k + ema * (1 - k)
        return ema

    def fake_adx(self, closes):
        """
        Simplified ADX approximation.
        """
        volatility = abs(closes[-1] - closes[-3])
        volatility_scaled = min(max(volatility * 5, 8), 35)
        return volatility_scaled

    # ------------------------------
    # REASON GENERATOR
    # ------------------------------

    def generate_reason(self, rsi, ema_fast, ema_slow, macd, adx, direction):
        reasons = []

        # RSI logic
        if rsi < 30 and direction == "BUY":
            reasons.append("RSI is oversold, increasing the chance of upward reversal.")
        elif rsi > 70 and direction == "SELL":
            reasons.append("RSI is overbought, showing downward correction potential.")

        # EMA crossover logic
        if ema_fast > ema_slow and direction == "BUY":
            reasons.append("Fast EMA is above slow EMA — bullish trend continuation.")
        elif ema_fast < ema_slow and direction == "SELL":
            reasons.append("Fast EMA is below slow EMA — bearish trend continuation.")

        # MACD logic
        if macd > 0 and direction == "BUY":
            reasons.append("MACD above zero confirms upward momentum.")
        elif macd < 0 and direction == "SELL":
            reasons.append("MACD below zero confirms downward pressure.")

        # ADX logic
        if adx > 20:
            reasons.append("Trend strength is healthy.")
        else:
            reasons.append("Trend is weak — movements may be sideways.")

        # Fallback
        if not reasons:
            return "Market conditions match the direction bias."

        return " ".join(reasons)

    # ------------------------------
    # CONFIDENCE SCORE
    # ------------------------------

    def calculate_confidence(self, rsi, ema_fast, ema_slow, macd, adx, direction):
        score = 50

        # RSI
        if direction == "BUY" and rsi < 30:
            score += 20
        if direction == "SELL" and rsi > 70:
            score += 20

        # EMA
        if direction == "BUY" and ema_fast > ema_slow:
            score += 15
        if direction == "SELL" and ema_fast < ema_slow:
            score += 15

        # MACD
        if direction == "BUY" and macd > 0:
            score += 10
        if direction == "SELL" and macd < 0:
            score += 10

        # ADX
        if adx > 20:
            score += 5

        return min(score, 100)
