import os

import pandas as pd
import yfinance as yf


def download_latest_data():

    print("=" * 60)
    print("BITCOIN HISTORICAL DATA DOWNLOADER")
    print("=" * 60)

    filename = "dataset/raw/btc_usd_yahoo_daily_full.csv"

    os.makedirs("dataset/raw", exist_ok=True)

    # =====================================================
    # CEK APAKAH DATASET SUDAH ADA
    # =====================================================

    if os.path.exists(filename):

        print("Membaca dataset lokal...")

        local_df = pd.read_csv(filename)
        local_df["Date"] = pd.to_datetime(local_df["Date"])

        local_last_date = local_df["Date"].max().date()

        print(f"Tanggal dataset lokal : {local_last_date}")

        print("\nMengecek Yahoo Finance...")

        latest = yf.download(
            "BTC-USD",
            period="5d",
            interval="1d",
            progress=False
        )

        if isinstance(latest.columns, pd.MultiIndex):
            latest.columns = latest.columns.get_level_values(0)

        latest.reset_index(inplace=True)

        latest_date = latest["Date"].max().date()

        print(f"Tanggal Yahoo Finance : {latest_date}")

        if local_last_date == latest_date:

            print("\nDataset sudah terbaru.")
            return False

        print("\nData baru ditemukan.")
        print("Mengunduh dataset terbaru...")

    else:

        print("Dataset belum ada.")
        print("Mengunduh dataset pertama kali...")

    # =====================================================
    # DOWNLOAD FULL DATASET
    # =====================================================

    btc = yf.download(
        "BTC-USD",
        period="max",
        interval="1d",
        progress=False
    )

    if isinstance(btc.columns, pd.MultiIndex):
        btc.columns = btc.columns.get_level_values(0)

    if btc.empty:
        print("Gagal mengambil data!")
        return False

    if "Adj Close" in btc.columns:
        btc = btc.drop(columns=["Adj Close"])

    btc.reset_index(inplace=True)

    btc.to_csv(filename, index=False)

    print("\nDataset berhasil diperbarui.")
    print(f"Jumlah Data : {len(btc)}")
    print(f"Tanggal Akhir : {btc['Date'].max()}")

    return True


if __name__ == "__main__":
    download_latest_data()