"""
=========================================================
Project  : Prediksi Harga Bitcoin Menggunakan LSTM
File     : train_model.py
Author   : Calvin Wijaya
Purpose  : Training Model LSTM
=========================================================
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import joblib

from tensorflow.keras import Input

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import LSTM, Dense, Dropout

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint
from config.training_config import *

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset" / "processed"

MODEL_DIR = BASE_DIR / "models"

DOC_DIR = BASE_DIR / "docs" / "training"

MODEL_DIR.mkdir(exist_ok=True)

DOC_DIR.mkdir(exist_ok=True)

X_train = np.load(DATASET_DIR / "X_train.npy")

y_train = np.load(DATASET_DIR / "y_train.npy")

X_test = np.load(DATASET_DIR / "X_test.npy")

y_test = np.load(DATASET_DIR / "y_test.npy")

print("="*60)
print("TRAIN MODEL LSTM")
print("="*60)

print()

print("Training")

print(X_train.shape)

print(y_train.shape)

print()

print("Testing")

print(X_test.shape)

print(y_test.shape)

print("\n" + "="*60)
print("MEMBANGUN MODEL LSTM")
print("="*60)

model = Sequential()

model.add(
    Input(
        shape=(X_train.shape[1], X_train.shape[2])
    )
)

model.add(
    LSTM(
        units=LSTM_LAYER_1,
        return_sequences=True
    )
)

model.add(Dropout(DROPOUT))

model.add(
    LSTM(
        units=LSTM_LAYER_2
    )
)

model.add(Dropout(DROPOUT))

model.add(Dense(16, activation="relu"))

model.add(Dense(1))

print()

model.summary()

model.compile(
    optimizer=OPTIMIZER,
    loss=LOSS_FUNCTION,
    metrics=["mae"]
)

print("\nModel berhasil di-compile.")

# =========================================================
# CALLBACK
# =========================================================

early_stopping = EarlyStopping(
    monitor="val_loss",
    mode="min",
    patience=10,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath=MODEL_DIR / "bitcoin_lstm.keras",
    monitor="val_loss",
    mode="min",
    save_best_only=True
)

# =========================================================
# TRAINING MODEL
# =========================================================

print("\n" + "="*60)
print("TRAINING MODEL")
print("="*60)

history = model.fit(
    X_train,
    y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    callbacks=[
        early_stopping,
        checkpoint
    ],
    verbose=1
)

print("\nTraining selesai.")

joblib.dump(
    history.history,
    MODEL_DIR / "training_history.pkl"
)

print("History training berhasil disimpan.")

print("\nModel terbaik disimpan di:")
print(MODEL_DIR / "bitcoin_lstm.keras")