import yfinance as yf
import pandas as pd

symbol = "INFY.NS"

# df = yf.download(symbol, start="2023-01-01", end="2026-01-01")
df = yf.download(symbol, period="1y")

df.reset_index(inplace=True)

df = df.rename(
    columns={
        "Date": "date",
        "Open": "open",
        "Close": "close",
        "High": "high",
        "Low": "low",
    }
)

df.ffill(inplace=True)

df["daily_return"] = (df["close"] - df["open"]) / df["open"]

df["ma_7"] = df["close"].rolling(window=7).mean()

df["52w_high"] = df["close"].rolling(window=252).max()
df["52w_low"] = df["close"].rolling(window=252).min()

df.to_csv(f"data/{symbol}.csv", index=False)

print(f"Successfully downloaded data for {symbol}")
