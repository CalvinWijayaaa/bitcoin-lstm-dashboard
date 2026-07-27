"""
=========================================================
Project : Prediksi Harga Bitcoin Menggunakan LSTM
File    : predict.py
Author  : Calvin Wijaya
Purpose : Prediksi Harga Bitcoin Hari Berikutnya
=========================================================
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from keras.models import load_model

# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "bitcoin_lstm.keras"

SCALER_PATH = BASE_DIR / "dataset" / "processed" / "scaler.pkl"

DATA_PATH = BASE_DIR / "dataset" / "raw" / "btc_usd_yahoo_daily_full.csv"

WINDOW_SIZE = 60

# =========================================================
# LOAD
# =========================================================

print("="*60)
print("PREDIKSI HARGA BITCOIN")
print("="*60)

model = load_model(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

df = pd.read_csv(DATA_PATH)

features = ["Open", "High", "Low", "Close", "Volume"]

data = df[features]

# =========================================================
# NORMALISASI
# =========================================================

scaled = scaler.transform(data)

# =========================================================
# AMBIL 60 HARI TERAKHIR
# =========================================================

last_sequence = scaled[-WINDOW_SIZE:]

X = np.array([last_sequence])

print(f"Shape Input : {X.shape}")

# =========================================================
# PREDIKSI
# =========================================================

prediction = model.predict(X, verbose=0)

# =========================================================
# KEMBALIKAN KE HARGA ASLI
# =========================================================

dummy = np.zeros((1, len(features)))

dummy[0, 3] = prediction[0, 0]

predicted_price = scaler.inverse_transform(dummy)[0, 3]

# =========================================================
# OUTPUT
# =========================================================

last_close = df.iloc[-1]["Close"]

print()

print(f"Harga Terakhir : ${last_close:,.2f}")

print(f"Prediksi Besok : ${predicted_price:,.2f}")

change = predicted_price - last_close

percent = (change / last_close) * 100

print(f"Selisih        : ${change:,.2f}")

print(f"Perubahan      : {percent:.2f}%")

print("="*60)