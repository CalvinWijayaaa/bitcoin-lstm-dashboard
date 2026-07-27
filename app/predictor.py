from pathlib import Path
from datetime import datetime, timedelta

import joblib
import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "bitcoin_lstm.keras"
SCALER_PATH = BASE_DIR / "dataset" / "processed" / "scaler.pkl"
DATA_PATH = BASE_DIR / "dataset" / "raw" / "btc_usd_yahoo_daily_full.csv"

WINDOW_SIZE = 60

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def get_prediction():

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["Date"]
    )
    

    features = ["Open", "High", "Low", "Close", "Volume"]

    data = df[features]

    scaled = scaler.transform(data)

    last_sequence = scaled[-WINDOW_SIZE:]

    X = np.array([last_sequence])

    prediction = model.predict(X, verbose=0)

    dummy = np.zeros((1, len(features)))

    dummy[0, 3] = prediction[0, 0]

    predicted_price = scaler.inverse_transform(dummy)[0, 3]

    last_price = df.iloc[-1]["Close"]
    
    last_data_date = df["Date"].iloc[-1].date()

    prediction_for_date = last_data_date + timedelta(days=1)

    change = predicted_price - last_price

    percent = (change / last_price) * 100

    trend = "Bullish" if change >= 0 else "Bearish"

    signal = "BUY" if change >= 0 else "SELL"

    return {

        "last_data_date": last_data_date,

        "prediction_for_date": prediction_for_date,

        "last_price": round(last_price,2),

        "prediction": round(predicted_price,2),

        "change": round(change,2),

        "percent": round(percent,2),

        "trend": trend,

        "signal": signal,

        "accuracy": 7.98,

        "updated": datetime.now().strftime("%d %B %Y %H:%M")
    }