import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from app.database import update_model_information
from config.training_config import *
from tensorflow.keras.models import load_model
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)

# =====================================================
# PATH PROJECT
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "bitcoin_lstm.keras")

SCALER_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "processed",
    "scaler.pkl"
)

X_TEST_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "processed",
    "X_test.npy"
)

Y_TEST_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "processed",
    "y_test.npy"
)

X_TRAIN_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "processed",
    "X_train.npy"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "docs",
    "training"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

print("=" * 50)
print("MEMUAT MODEL DAN DATA...")
print("=" * 50)

model = load_model(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

X_test = np.load(X_TEST_PATH)

y_test = np.load(Y_TEST_PATH)

print(f"Jumlah data testing : {len(X_test)}")

# =====================================================
# PREDIKSI
# =====================================================

print("\nMelakukan prediksi...")

prediction = model.predict(X_test, verbose=0)

# =====================================================
# INVERSE TRANSFORM KHUSUS KOLOM CLOSE
# =====================================================

def inverse_close(scaler, values):
    dummy = np.zeros((len(values), 5))
    dummy[:, 3] = values.flatten()   # kolom Close
    return scaler.inverse_transform(dummy)[:, 3]

prediction = inverse_close(scaler, prediction)

actual = inverse_close(
    scaler,
    y_test.reshape(-1, 1)
)

# =====================================================
# EVALUASI
# =====================================================

mae = mean_absolute_error(actual, prediction)

mse = mean_squared_error(actual, prediction)

rmse = np.sqrt(mse)

mape = mean_absolute_percentage_error(actual, prediction) * 100

print("\n" + "=" * 50)
print("HASIL EVALUASI MODEL")
print("=" * 50)

print(f"MAE  : {mae:,.2f}")

print(f"MSE  : {mse:,.2f}")

print(f"RMSE : {rmse:,.2f}")

print(f"MAPE : {mape:.2f}%")

# =====================================================
# SIMPAN CSV
# =====================================================

hasil = pd.DataFrame({
    "Actual": actual.flatten(),
    "Prediction": prediction.flatten()
})

evaluation_result = {

    "algorithm": ALGORITHM,

    "dataset": DATASET_NAME,

    "window_size": WINDOW_SIZE,

    "epochs": EPOCHS,

    "features": ", ".join(FEATURES),

    "optimizer": OPTIMIZER,

    "loss_function": LOSS_FUNCTION,

    "mae": float(mae),

    "rmse": float(rmse),

    "mape": float(mape),

    "training_samples": len(np.load(X_TRAIN_PATH)),

    "testing_samples": len(X_test)

}

csv_path = os.path.join(
    OUTPUT_DIR,
    "prediction_result.csv"
)

hasil.to_csv(csv_path, index=False)

# =====================================================
# VISUALISASI
# =====================================================

plt.figure(figsize=(15,6))

plt.plot(actual, label="Actual Price")

plt.plot(prediction, label="Predicted Price")

plt.title("Bitcoin Price Prediction (Testing Data)")

plt.xlabel("Time")

plt.ylabel("Price (USD)")

plt.legend()

plt.grid(True)

plot_path = os.path.join(
    OUTPUT_DIR,
    "prediction_result.png"
)

plt.savefig(plot_path, dpi=300)

plt.show()

print("\nGrafik berhasil disimpan.")

print(plot_path)

print(csv_path)

print("\nEvaluasi selesai.")

def get_evaluation_result():
    """
    Mengembalikan hasil evaluasi model
    agar dapat digunakan script lain.
    """

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "mape": float(mape),
        "testing_samples": len(X_test)
    }
    
print("\nEvaluation Result")

print(evaluation_result)

update_model_information(evaluation_result)

print()

print("Model Information berhasil diperbarui.")

PROCESSED_DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "processed"
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

DOC_DIR = os.path.join(BASE_DIR, "docs", "training")

MODEL_PATH = os.path.join(MODEL_DIR, "bitcoin_lstm.keras")

SCALER_PATH = os.path.join(PROCESSED_DATASET_DIR, "scaler.pkl")

X_TRAIN_PATH = os.path.join(PROCESSED_DATASET_DIR, "X_train.npy")

X_TEST_PATH = os.path.join(PROCESSED_DATASET_DIR, "X_test.npy")

Y_TEST_PATH = os.path.join(PROCESSED_DATASET_DIR, "y_test.npy")