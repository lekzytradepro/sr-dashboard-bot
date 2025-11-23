# core/ai_signal_engine.py

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from config.global_config import TWELVE_DATA_API_KEY, TWELVE_DATA_BASE_URL

class AISignalEngine:
    def __init__(self):
        self.api_key = TWELVE_DATA_API_KEY
        self.base_url = TWELVE_DATA_BASE_URL

    def fetch_data(self, symbol):
        """Fetch OHLC data from TwelveData API"""
        url = f"{self.base_url}/time_series?symbol={symbol}&interval=1min&outputsize=60&apikey={self.api_key}"
        try:
            r = requests.get(url)
            raw = r.json()

            if "values" not in raw:
                return None

            df = pd.DataFrame(raw["values"])
            df["close"] = df["close"].astype(float)
            df = df[::-1].reset_index(drop=True)
            return df

        except Exception:
            return None

    # =========================
    # Indicator Calculations
    # =========================
    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return (100 - (100 / (1 + rs))).iloc[-1]

    def calculate_macd(self, prices):
        ema12 = prices.ewm(span=12, adjust=False).mean()
        ema26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd.iloc[-1], signal.iloc[-1]

    def calculate_ema(self, prices, period):
        return prices.ewm(span=period, adjust=False).mean().iloc[-1]

    # =========================
    # AI-Based Signal Decision
    # =========================
    def generate_signal(self, asset):
        df = self.fetch_data(asset)
        if df is None or len(df) < 40:
            return {
                "asset": asset,
                "direction": "NEUTRAL",
                "confidence": 45,
                "reason": "Not enough market data",
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }

        prices = df["close"]

        # Indicators
        rsi = self.calculate_rsi(prices)
        macd, signal = self.calculate_macd(prices)
        ema20 = self.calculate_ema(prices, 20)
        ema50 = self.calculate_ema(prices, 50)
        trend_strength = abs(macd - signal) * 100

        # ============================================
        # SIGNAL LOGIC (Professional-level logic)
        # ============================================

        if rsi < 30 and macd > signal and ema20 > ema50:
            direction = "BUY"
            confidence = min(95, 65 + trend_strength)

        elif rsi > 70 and macd < signal and ema20 < ema50:
            direction = "SELL"
            confidence = min(95, 65 + trend_strength)

        else:
            direction = "NEUTRAL"
            confidence = 50

        return {
            "asset": asset,
            "direction": direction,
            "confidence": round(confidence, 2),
            "rsi": round(rsi, 2),
            "macd": round(macd, 5),
            "signal_line": round(signal, 5),
            "ema20": round(ema20, 5),
            "ema50": round(ema50, 5),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
      }
