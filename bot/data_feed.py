# bot/data_feed.py
import aiohttp
import json
from typing import List, Dict, Optional

class DataFeed:
    """
    Fetch candles for ANY asset & timeframe.
    Works with Exnova/Quotex compatible API format.
    """

    def __init__(self, asset: str, timeframe="1m"):
        self.asset = asset.upper()
        self.timeframe = timeframe

    async def get_candles(self, limit=200) -> Optional[List[Dict]]:
        """
        Fetch OHLC candle data from public API.
        Returns a list of dictionaries (no pandas needed).
        """

        url = f"https://api.exnova.live/v1/candles?asset={self.asset}&tf={self.timeframe}&limit={limit}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    raw = await res.json()

            # Convert to list of dictionaries with proper naming
            candles = []
            for candle in raw:
                candles.append({
                    "open": float(candle["o"]),
                    "high": float(candle["h"]),
                    "low": float(candle["l"]),
                    "close": float(candle["c"]),
                    "timestamp": int(candle["t"])
                })

            return candles

        except Exception as e:
            print("DataFeed Error:", e)
            return None

    async def get_last_close(self) -> Optional[float]:
        """
        Quick helper to get only latest close price.
        """
        candles = await self.get_candles(limit=1)
        if not candles:
            return None
        return candles[-1]["close"]

    async def get_dataframe_simulation(self, limit=200):
        """
        If you need DataFrame-like access, this provides similar functionality.
        """
        candles = await self.get_candles(limit)
        if not candles:
            return None
        
        # Example: Get all close prices (like df['close'])
        close_prices = [candle["close"] for candle in candles]
        # Example: Get last candle (like df.iloc[-1])
        last_candle = candles[-1] if candles else None
        
        return {
            "candles": candles,
            "close_prices": close_prices,
            "last_candle": last_candle
        }
