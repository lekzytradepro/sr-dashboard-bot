# bot/data_feed.py

import pandas as pd
import aiohttp

class DataFeed:
    """
    Fetch candles for ANY asset & timeframe.
    Works with Exnova/Quotex compatible API format.
    """

    def __init__(self, asset: str, timeframe="1m"):
        self.asset = asset.upper()
        self.timeframe = timeframe

    async def get_candles(self, limit=200):
        """
        Fetch OHLC candle data from public API.
        Returns a pandas DataFrame.
        """

        url = f"https://api.exnova.live/v1/candles?asset={self.asset}&tf={self.timeframe}&limit={limit}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    raw = await res.json()

            df = pd.DataFrame(raw)

            df.rename(columns={
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "t": "timestamp"
            }, inplace=True)

            df = df.astype({
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "timestamp": int
            })

            return df

        except Exception as e:
            print("DataFeed Error:", e)
            return None

    async def get_last_close(self):
        """
        Quick helper to get only latest close price.
        """
        df = await self.get_candles(limit=1)
        if df is None or df.empty:
            return None
        return df["close"].iloc[-1]
