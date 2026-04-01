from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

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

    if not symbol.endswith(".NS"):
        symbol = symbol + ".NS"

    # file_path = f"{DATA_FOLDER}/{symbol}.csv"

    file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")

    if not os.path.exists(file_path):
        return {"error": "Stock not found"}

    df = pd.read_csv(file_path)

    df = df.tail(30)
    df = df.fillna(0)

    return {"symbol": symbol, "data": df.to_dict(orient="records")}
