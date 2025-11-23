import pandas as pd
from bot.indicators.technical_indicators import TechnicalIndicators

class MarketDataProcessor:

    def __init__(self):
        pass

    def to_dataframe(self, raw_data):
        """
        Convert TwelveData API data into a clean dataframe.
        """
        df = pd.DataFrame(raw_data)
        df = df.rename(columns={
            'datetime': 'time',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close'
        })

        # Convert numeric columns
        numeric_cols = ['open', 'high', 'low', 'close']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['time'] = pd.to_datetime(df['time'])

        # Sort candles
        df = df.sort_values('time')

        # Drop any missing rows
        df = df.dropna()

        return df

    def add_indicators(self, df):
        """
        Apply all technical indicators to the dataframe.
        """
        indicators = TechnicalIndicators(df)
        df = indicators.rsi()
        df = indicators.sma()
        df = indicators.ema()
        df = indicators.macd()
        df = indicators.bollinger()

        return df

    def prepare(self, raw_data):
        """
        Full preparation pipeline.
        """
        df = self.to_dataframe(raw_data)
        df = self.add_indicators(df)

        # Keep last 300 candles (fast performance)
        df = df.tail(300)

        return df
