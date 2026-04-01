from fastapi import FastAPI
import pandas as pd
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data")


@app.get("/")
def read_root():
    return {"message": "Stock Dashboard API is running 🚀"}


@app.get("/companies")
def get_companies():
    files = os.listdir(DATA_FOLDER)
    companies = [f.replace(".csv", "") for f in files]
    return {"companies": companies}


@app.get("/data/{symbol}")
def get_stock_data(symbol: str):

    symbol = symbol.strip().upper()

    if ".NS" not in symbol:
        symbol += ".NS"

    print("Requested symbol:", symbol)

    file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")

    if not os.path.exists(file_path):
        return {"error": f"{symbol} not found"}

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()

    df = df.tail(30)
    df = df.fillna(0)

    return {"symbol": symbol, "data": df.to_dict(orient="records")}


@app.get("/summary/{symbol}")
def get_summary(symbol: str):

    symbol = symbol.strip().upper()

    if ".NS" not in symbol:
        symbol += ".NS"

    print("Requested symbol:", symbol)

    file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")

    if not os.path.exists(file_path):
        return {"error": f"{symbol} not found"}

    df = pd.read_csv(file_path)

    df.columns = df.columns.str.lower()
    df = df[["open", "close", "high", "low"]]
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.ffill()

    return {
        "symbol": symbol,
        "52w_high": float(df["high"].max()),
        "52w_low": float(df["low"].min()),
        "avg_close": float(df["close"].mean()),
    }


@app.get("/compare")
def compare_stocks(symbol1: str, symbol2: str):

    def get_data(symbol):
        symbol = symbol.strip().upper()

        if ".NS" not in symbol:
            symbol += ".NS"

        file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")

        print("Requested symbol:", symbol)

        if not os.path.exists(file_path):
            return None, symbol

        df = pd.read_csv(file_path)

        df.columns = df.columns.str.lower()

        df = df[["open", "close", "high", "low"]]

        df = df.apply(pd.to_numeric, errors="coerce")

        df = df.dropna()

        return df, symbol

    df1, s1 = get_data(symbol1)
    df2, s2 = get_data(symbol2)

    if df1 is None or df2 is None:
        return {"error": "One or both stocks not found"}

    if df1.empty or df2.empty:
        return {"error": "Stock data is empty"}

    avg1 = df1["close"].mean()
    avg2 = df2["close"].mean()

    trend1 = "upward" if df1["close"].iloc[-1] > avg1 else "downward"
    trend2 = "upward" if df2["close"].iloc[-1] > avg2 else "downward"

    return {
        "stock1": {"symbol": s1, "avg": float(avg1), "trend": trend1},
        "stock2": {"symbol": s2, "avg": float(avg2), "trend": trend2},
    }
