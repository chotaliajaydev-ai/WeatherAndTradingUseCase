"""
tradingweather.py

A use-case script that fetches current weather data for a given city and
retrieves recent stock price data for a given ticker symbol, then prints a
simple weather-based trading signal.

Dependencies:
    pip install requests yfinance

Environment variables (or hard-coded defaults for demo):
    OPENWEATHER_API_KEY  – API key from https://openweathermap.org/api
"""

import os
import sys
import datetime

import requests
import yfinance as yf


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ---------------------------------------------------------------------------
# Weather helpers
# ---------------------------------------------------------------------------

def get_weather(city: str) -> dict:
    """Fetch current weather for *city* from OpenWeatherMap.

    Returns a dict with keys: city, temperature_c, description, humidity.
    Raises RuntimeError on API or network errors.
    """
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }
    response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(
            f"Weather API error {response.status_code}: {response.text}"
        )
    data = response.json()
    return {
        "city": data["name"],
        "temperature_c": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
    }


# ---------------------------------------------------------------------------
# Trading helpers
# ---------------------------------------------------------------------------

def get_stock_data(ticker: str, period: str = "5d") -> dict:
    """Fetch recent closing prices for *ticker* using yfinance.

    Returns a dict with keys: ticker, latest_close, previous_close,
    change_pct, period.
    Raises ValueError if no data is returned.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    if hist.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'")
    latest_close = hist["Close"].iloc[-1]
    previous_close = hist["Close"].iloc[-2] if len(hist) > 1 else latest_close
    change_pct = ((latest_close - previous_close) / previous_close) * 100
    return {
        "ticker": ticker.upper(),
        "latest_close": round(latest_close, 2),
        "previous_close": round(previous_close, 2),
        "change_pct": round(change_pct, 2),
        "period": period,
    }


# ---------------------------------------------------------------------------
# Signal logic
# ---------------------------------------------------------------------------

def weather_trading_signal(weather: dict, stock: dict) -> str:
    """Return a simple trading signal based on weather and price trend.

    Rules (illustrative only – not financial advice):
      - Clear sky  + price rising  → "BUY"
      - Rain/storm + price falling → "SELL"
      - Anything else              → "HOLD"
    """
    description = weather["description"].lower()
    change_pct = stock["change_pct"]

    positive_weather = any(
        word in description for word in ("clear", "sunny", "fair")
    )
    negative_weather = any(
        word in description for word in ("rain", "storm", "thunder", "drizzle", "snow")
    )

    if positive_weather and change_pct > 0:
        return "BUY"
    if negative_weather and change_pct < 0:
        return "SELL"
    return "HOLD"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(city: str = "London", ticker: str = "AAPL") -> None:
    print("=" * 60)
    print(f"  Weather & Trading Use Case  –  {datetime.date.today()}")
    print("=" * 60)

    # --- Weather ---
    print(f"\nFetching weather for: {city}")
    weather = get_weather(city)
    print(f"  City        : {weather['city']}")
    print(f"  Temperature : {weather['temperature_c']} °C")
    print(f"  Conditions  : {weather['description']}")
    print(f"  Humidity    : {weather['humidity']} %")

    # --- Stock ---
    print(f"\nFetching stock data for: {ticker}")
    stock = get_stock_data(ticker)
    print(f"  Ticker      : {stock['ticker']}")
    print(f"  Latest close: ${stock['latest_close']}")
    print(f"  Prev close  : ${stock['previous_close']}")
    print(f"  Change      : {stock['change_pct']:+.2f} %")

    # --- Signal ---
    signal = weather_trading_signal(weather, stock)
    print(f"\n{'─' * 60}")
    print(f"  Weather-based trading signal: {signal}")
    print(f"{'─' * 60}\n")
    print("Disclaimer: This is for educational purposes only.")
    print("It is NOT financial advice.")


if __name__ == "__main__":
    _city = sys.argv[1] if len(sys.argv) > 1 else "London"
    _ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
    main(_city, _ticker)
