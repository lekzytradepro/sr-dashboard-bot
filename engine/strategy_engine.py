# engine/strategy_engine.py

class StrategyEngine:
    def __init__(self, df):
        self.df = df

    def generate_signal(self):
        """
        Simple strategy:
        - BUY if RSI < 30 and macd > macd_signal
        - SELL if RSI > 70 and macd < macd_signal
        - NEUTRAL otherwise
        """

        try:
            rsi = self.df['rsi'].iloc[-1]
            macd = self.df['macd'].iloc[-1]
            macd_sig = self.df['macd_signal'].iloc[-1]

            # BUY Signal
            if rsi < 30 and macd > macd_sig:
                return "BUY"

            # SELL Signal
            elif rsi > 70 and macd < macd_sig:
                return "SELL"

            # Otherwise NEUTRAL
            else:
                return "NEUTRAL"

        except Exception as e:
            print("Strategy Engine Error:", e)
            return "NEUTRAL"
