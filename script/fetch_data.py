import yfinance as yf
import pandas as pd

symbol = "INFY.NS"

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

df["52w_high"] = df["high"].rolling(window=252).max()
df["52w_low"] = df["low"].rolling(window=252).min()

df.to_csv(f"data/{symbol}.csv", index=False)

print(f"Successfully downloaded data for {symbol}")
