# WeatherAndTradingUseCase

A Python use-case that combines **real-time weather data** with **stock market data** to generate a simple, illustrative trading signal.

> ⚠️ **Disclaimer:** This project is for educational purposes only. It is **not** financial advice.

---

## Features

- Fetches current weather conditions for any city via the [OpenWeatherMap API](https://openweathermap.org/api)
- Retrieves recent stock closing prices using [yfinance](https://github.com/ranaroussi/yfinance)
- Combines both data sources to produce a weather-based trading signal (`BUY` / `SELL` / `HOLD`)

---

## Requirements

- Python 3.8+
- [requests](https://pypi.org/project/requests/)
- [yfinance](https://pypi.org/project/yfinance/)

Install dependencies:

```bash
pip install requests yfinance
```

---

## Setup

1. Obtain a free API key from <https://openweathermap.org/api>.
2. Export it as an environment variable:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

---

## Usage

```bash
python tradingweather.py [CITY] [TICKER]
```

| Argument | Default  | Description                          |
|----------|----------|--------------------------------------|
| `CITY`   | `London` | City name for weather lookup         |
| `TICKER` | `AAPL`   | Stock ticker symbol (e.g. TSLA, MSFT)|

### Example

```bash
python tradingweather.py "New York" TSLA
```

**Sample output:**

```
============================================================
  Weather & Trading Use Case  –  2024-06-01
============================================================

Fetching weather for: New York
  City        : New York
  Temperature : 22.5 °C
  Conditions  : clear sky
  Humidity    : 55 %

Fetching stock data for: TSLA
  Ticker      : TSLA
  Latest close: $182.45
  Prev close  : $178.90
  Change      : +1.98 %

────────────────────────────────────────────────────────────
  Weather-based trading signal: BUY
────────────────────────────────────────────────────────────

Disclaimer: This is for educational purposes only.
It is NOT financial advice.
```

---

## Signal Logic

| Weather Condition         | Price Trend | Signal |
|---------------------------|-------------|--------|
| Clear / Sunny / Fair      | Rising      | BUY    |
| Rain / Storm / Drizzle    | Falling     | SELL   |
| Anything else             | Any         | HOLD   |

---

## File Structure

```
WeatherAndTradingUseCase/
├── tradingweather.py   # Main script
└── README.md
```
