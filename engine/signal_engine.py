class SignalEngine:
    def __init__(self, analyzer):
        self.data = analyzer

    def generate(self):
        trend = self.data.trend_direction()
        danger = self.data.detect_danger()

        if danger:
            return "NEUTRAL", 0.0, "High volatility"

        if trend == "up":
            return "BUY", 0.87, "Trend continuation"

        if trend == "down":
            return "SELL", 0.83, "Strong downward momentum"

        return "NEUTRAL", 0.55, "Sideways market"
