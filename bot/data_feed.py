# bot/data_feed.py

import requests
import time


class DataFeed:
    """
    Simple candle fetcher for any asset.
    You can later switch to Binance, Forex, or your custom API.
    """

    def __init__(self):
        self.api_url = "https://api.binance.com/api/v3/klines"

    def get_candles(self, symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 50):
        """
        Fetch OHLC candle data.
        Returns list of candles in this structure:
        [
            {
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float,
                "timestamp": int
            }
        ]
        """

        try:
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }

            response = requests.get(self.api_url, params=params, timeout=5)
            data = response.json()

            candles = []

            for c in data:
                candles.append({
                    "timestamp": int(c[0]),
                    "open": float(c[1]),
                    "high": float(c[2]),
                    "low": float(c[3]),
                    "close": float(c[4]),
                    "volume": float(c[5])
                })

            return candles

        except Exception:
            return None

    def get_latest_price(self, symbol="BTCUSDT"):
        """
        Fetch only the latest close price.
        """

        candles = self.get_candles(symbol, "1m", 1)
        if not candles:
            return None

        return candles[-1]["close"]
