"""
=========================================================
Project  : Prediksi Harga Bitcoin Menggunakan LSTM
File     : eda.py
Author   : Calvin Wijaya
Purpose  : Exploratory Data Analysis (EDA)
=========================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# =========================================================
# MEMBACA DATASET
# =========================================================

# Folder utama project
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "raw" / "btc_usd_yahoo_daily_full.csv"

OUTPUT_DIR = BASE_DIR / "docs" / "eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Mengubah kolom Date menjadi tipe datetime
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# =========================================================
# MENAMPILKAN 5 DATA PERTAMA
# =========================================================

print("\n1. Lima Data Pertama")
print("-" * 60)
print(df.head())

# =========================================================
# INFORMASI DATASET
# =========================================================

print("\n2. Informasi Dataset")
print("-" * 60)

df.info()

# =========================================================
# STATISTIK DESKRIPTIF
# =========================================================

print("\n3. Statistik Deskriptif")
print("-" * 60)

print(df.describe())

# =========================================================
# MISSING VALUE
# =========================================================

print("\n4. Missing Value")
print("-" * 60)

print(df.isnull().sum())

print("\nEDA Tahap 1 Selesai")

# =========================================================
# GRAFIK HARGA BITCOIN
# =========================================================

plt.figure(figsize=(15,6))

plt.plot(
    df["Date"],
    df["Close"],
    color="royalblue",
    linewidth=2,
    label="Close Price"
)

# =========================================================
# GARIS HALVING
# =========================================================

plt.axvline(
    pd.Timestamp("2016-07-09"),
    color="red",
    linestyle="--",
    linewidth=2,
)

plt.text(
    pd.Timestamp("2016-07-09"),
    df["Close"].max()*0.97,
    "Halving 2016",
    rotation=90,
    color="red",
    fontsize=9,
    ha="right",
    va="top"
)

plt.axvline(
    pd.Timestamp("2020-05-11"),
    color="green",
    linestyle="--",
    linewidth=2,
)

plt.text(
    pd.Timestamp("2020-05-11"),
    df["Close"].max()*0.97,
    "Halving 2020",
    rotation=90,
    color="green",
    fontsize=9,
    ha="right",
    va="top"
)

plt.axvline(
    pd.Timestamp("2024-04-20"),
    color="orange",
    linestyle="--",
    linewidth=2,
)

plt.text(
    pd.Timestamp("2024-04-20"),
    df["Close"].max()*0.97,
    "Halving 2024",
    rotation=90,
    color="orange",
    fontsize=9,
    ha="right",
    va="top"
)

plt.legend(loc="upper left")

plt.title(
    "Historical Bitcoin Closing Price (2014–2026)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Date", fontsize=12)
plt.ylabel("Price (USD)", fontsize=12)

plt.grid(alpha=0.3, linestyle="--")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "01_close_price.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Grafik Close Price berhasil disimpan.")

# =========================================================
# GRAFIK VOLUME
# =========================================================

plt.figure(figsize=(15,6))

plt.plot(
    df["Date"],
    df["Volume"],
    color="darkorange",
    linewidth=1.5
)

plt.title(
    "Bitcoin Trading Volume (2014–2026)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Date", fontsize=12)

plt.ylabel("Volume", fontsize=12)

plt.grid(alpha=0.3, linestyle="--")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "02_volume.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Grafik Volume berhasil disimpan.")

# =========================================================
# HISTOGRAM CLOSE PRICE
# =========================================================

plt.figure(figsize=(10,6))

plt.hist(
    df["Close"],
    bins=50,
    color="royalblue",
    edgecolor="black"
)

plt.title(
    "Distribution of Bitcoin Closing Price",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Closing Price (USD)")
plt.ylabel("Frequency")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "03_histogram_close.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Histogram berhasil disimpan.")

# =========================================================
# BOXPLOT CLOSE PRICE
# =========================================================

plt.figure(figsize=(8,6))

plt.boxplot(df["Close"])

plt.title(
    "Boxplot of Bitcoin Closing Price",
    fontsize=16,
    fontweight="bold"
)

plt.ylabel("Price (USD)")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "04_boxplot_close.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Boxplot berhasil disimpan.")

# =========================================================
# CORRELATION HEATMAP
# =========================================================

plt.figure(figsize=(8,6))

correlation = df[["Open", "High", "Low", "Close", "Volume"]].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5,
    fmt=".2f"
)

plt.title(
    "Correlation Heatmap",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "05_correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Heatmap berhasil disimpan.")