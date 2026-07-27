"""
=========================================================
Project  : Prediksi Harga Bitcoin Menggunakan LSTM
File     : preprocessing.py
Author   : Calvin Wijaya
Purpose  : Data Preprocessing
=========================================================
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "raw" / "btc_usd_yahoo_daily_full.csv"

OUTPUT_DIR = BASE_DIR / "dataset" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# PARAMETER MODEL
# =========================================================

WINDOW_SIZE = 60


# =========================================================
# MEMBUAT SEQUENCE
# =========================================================

def create_sequences(data, window_size):

    X = []
    y = []

    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])

        # Target adalah kolom Close
        y.append(data[i, 3])

    return np.array(X), np.array(y)


# =========================================================
# PREPROCESS DATA
# =========================================================

def preprocess_data():

    # =====================================================
    # MEMBACA DATASET
    # =====================================================

    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(df["Date"])

    print("=" * 60)
    print("PREPROCESSING DATASET")
    print("=" * 60)

    print(df.head())

    # =====================================================
    # MEMILIH FITUR
    # =====================================================

    features = ["Open", "High", "Low", "Close", "Volume"]

    data = df[features]

    print("\nFitur yang digunakan:")

    print(data.head())

    # =====================================================
    # TRAIN TEST SPLIT
    # =====================================================

    train_size = int(len(data) * 0.8)

    train_data = data.iloc[:train_size]

    test_data = data.iloc[train_size:]

    print("\n" + "=" * 60)
    print("TRAIN TEST SPLIT")
    print("=" * 60)

    print(f"Jumlah Data Training : {len(train_data)}")
    print(f"Jumlah Data Testing  : {len(test_data)}")

    # =====================================================
    # NORMALISASI
    # =====================================================

    scaler = MinMaxScaler()

    train_scaled = scaler.fit_transform(train_data)

    test_scaled = scaler.transform(test_data)

    print("\nNormalisasi berhasil.")

    joblib.dump(
        scaler,
        OUTPUT_DIR / "scaler.pkl"
    )

    print("Scaler berhasil disimpan.")

    train_scaled_df = pd.DataFrame(
        train_scaled,
        columns=features
    )

    test_scaled_df = pd.DataFrame(
        test_scaled,
        columns=features
    )

    train_scaled_df.to_csv(
        OUTPUT_DIR / "train_scaled.csv",
        index=False
    )

    test_scaled_df.to_csv(
        OUTPUT_DIR / "test_scaled.csv",
        index=False
    )

    print("Training dan Testing berhasil disimpan.")

    # =====================================================
    # MEMBUAT DATA LSTM
    # =====================================================

    X_train, y_train = create_sequences(
        train_scaled,
        WINDOW_SIZE
    )

    X_test, y_test = create_sequences(
        test_scaled,
        WINDOW_SIZE
    )

    print("\n" + "=" * 60)
    print("LSTM DATASET")
    print("=" * 60)

    print(f"X_train : {X_train.shape}")

    print(f"y_train : {y_train.shape}")

    print(f"X_test  : {X_test.shape}")

    print(f"y_test  : {y_test.shape}")

    np.save(
        OUTPUT_DIR / "X_train.npy",
        X_train
    )

    np.save(
        OUTPUT_DIR / "X_test.npy",
        X_test
    )

    np.save(
        OUTPUT_DIR / "y_train.npy",
        y_train
    )

    np.save(
        OUTPUT_DIR / "y_test.npy",
        y_test
    )

    print("\nSequence berhasil disimpan.")

    return True


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    preprocess_data()