import os, time, json, math
import pandas as pd
import yfinance as yf
'''
Fetch real-time market data for a given ticker, including price, volume, and technical indicators.
'''

def fetch_market_snapshot(ticker: str, period="1y", interval="1d"):
    tk = yf.Ticker(ticker)
    info = tk.fast_info  # fast price/volume snapshot
    hist = tk.history(period=period, interval=interval)

    # Compute SMA50 / SMA200
    hist["SMA50"]  = hist["Close"].rolling(window=50).mean()
    hist["SMA200"] = hist["Close"].rolling(window=200).mean()

    snapshot = {
        "ticker": ticker.upper(),
        "price": float(info["last_price"]) if "last_price" in info else float(hist["Close"].iloc[-1]),
        "day_high": float(info.get("day_high", float("nan"))),
        "day_low": float(info.get("day_low", float("nan"))),
        "volume": int(info.get("last_volume", 0)),
        "sma50": float(hist["SMA50"].iloc[-1]) if not math.isnan(hist["SMA50"].iloc[-1]) else None,
        "sma200": float(hist["SMA200"].iloc[-1]) if not math.isnan(hist["SMA200"].iloc[-1]) else None,
    }
    return snapshot, hist