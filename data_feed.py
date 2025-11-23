import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWELVEDATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"


def fetch_candles(symbol: str, interval: str = "1h", output_size: int = 300):
    """
    Fetch OHLC data for a given pair.
    """
    url = f"{BASE_URL}/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": API_KEY,
        "outputsize": output_size
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    if "values" not in data:
        return None

    return data["values"]
