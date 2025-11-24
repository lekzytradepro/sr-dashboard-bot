# core/signal_processor.py

import pandas as pd
from bot.indicators.technical_indicators import TechnicalIndicators
from engine.strategy_engine import StrategyEngine
from storage.signal_storage import SignalStorage

class SignalProcessor:
    def __init__(self):
        self.storage = SignalStorage()

    def process(self, df: pd.DataFrame):
        """
        Full processing of raw OHLCV data:
        - Add indicators
        - Apply strategy engine
        - Save signal to storage
        """
        try:
            # 1. Apply indicators
            ti = TechnicalIndicators(df)
            df = ti.rsi()
            df = ti.macd()
            df = ti.bollinger()

            # 2. Evaluate strategy
            strategy = StrategyEngine(df)
            final_signal = strategy.generate_signal()

            # 3. Store the processed signal
            self.storage.save_signal(final_signal)

            return final_signal

        except Exception as e:
            print("Signal Processing Error:", e)
            return "NEUTRAL"
