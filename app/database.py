import pymysql
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "4000")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor,
    "ssl": {
        "ca": str(BASE_DIR / "isrgrootx1.pem")
    }
}

def get_prediction_result():

    csv_path = (
        BASE_DIR
        / "docs"
        / "training"
        / "prediction_result.csv"
    )

    if not csv_path.exists():
        return [], []

    df = pd.read_csv(csv_path)

    actual = df["Actual"].tolist()

    prediction = df["Prediction"].tolist()

    return actual, prediction

def connect_db():
    """
    Membuat koneksi ke database MySQL.
    """
    return pymysql.connect(**DB_CONFIG)

from datetime import datetime


def save_prediction(data):
    """
    Menyimpan hasil prediksi.
    Jika prediction_for_date sudah ada -> UPDATE
    Jika belum ada -> INSERT
    """

    conn = connect_db()
    cursor = conn.cursor()

    # ============================
    # Cek apakah tanggal prediksi sudah ada
    # ============================

    cursor.execute(
        """
        SELECT id
        FROM prediction_history
        WHERE prediction_for_date = %s
        """,
        (data["prediction_for_date"],)
    )

    result = cursor.fetchone()

    # ============================
    # UPDATE
    # ============================

    if result:

        sql = """
        UPDATE prediction_history
        SET
            prediction_date = %s,
            last_data_date = %s,
            last_price = %s,
            predicted_price = %s,
            price_change = %s,
            percentage_change = %s,
            trend = %s,
            trade_signal = %s
        WHERE prediction_for_date = %s
        """

        cursor.execute(
            sql,
            (
                datetime.now(),
                data["last_data_date"],
                data["last_price"],
                data["prediction"],
                data["change"],
                data["percent"],
                data["trend"],
                data["signal"],
                data["prediction_for_date"]
            )
        )

        print("Prediction berhasil di-update.")

    # ============================
    # INSERT
    # ============================

    else:

        sql = """
        INSERT INTO prediction_history
        (
            id,
            prediction_date,
            last_data_date,
            prediction_for_date,
            last_price,
            predicted_price,
            price_change,
            percentage_change,
            trend,
            trade_signal
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """
        
        cursor.execute("""
        SELECT COALESCE(MAX(id),0)+1 AS next_id
        FROM prediction_history
        """)

        next_id = cursor.fetchone()["next_id"]

        cursor.execute(
            sql,
            (
                next_id,
                datetime.now(),
                data["last_data_date"],
                data["prediction_for_date"],
                data["last_price"],
                data["prediction"],
                data["change"],
                data["percent"],
                data["trend"],
                data["signal"]
            )
        )

        print("Prediction berhasil disimpan.")

    conn.commit()
    conn.close()
    
def get_latest_prediction():
    """
    Mengambil hasil prediksi terbaru.
    """

    conn = connect_db()

    cursor = conn.cursor()

    sql = """
        SELECT *
        FROM prediction_history
        ORDER BY id DESC
        LIMIT 1
    """

    cursor.execute(sql)

    data = cursor.fetchone()

    conn.close()

    return data

def get_prediction_history():

    conn = connect_db()

    cursor = conn.cursor()

    sql = """
        SELECT *
        FROM prediction_history
        ORDER BY prediction_date DESC
    """

    cursor.execute(sql)

    data = cursor.fetchall()

    conn.close()

    return data

from datetime import date

def has_prediction_today():

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
        SELECT COUNT(*) AS total
        FROM prediction_history
        WHERE DATE(prediction_date) = CURDATE()
    """

    cursor.execute(sql)

    result = cursor.fetchone()

    conn.close()

    return result["total"] > 0

def get_model_information():
    """
    Mengambil informasi model LSTM terbaru.
    """

    conn = connect_db()

    cursor = conn.cursor()

    sql = """
        SELECT *
        FROM model_information
        ORDER BY id DESC
        LIMIT 1
    """

    cursor.execute(sql)

    data = cursor.fetchone()

    conn.close()

    return data

def update_model_information(result):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM model_information")

    sql = """
    INSERT INTO model_information
    (
        algorithm,
        dataset,
        window_size,
        epochs,
        features,
        optimizer,
        loss_function,
        mae,
        rmse,
        mape,
        training_samples,
        testing_samples,
        training_date
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())
    """

    cursor.execute(
        sql,
        (
            result["algorithm"],
            result["dataset"],
            result["window_size"],
            result["epochs"],
            result["features"],
            result["optimizer"],
            result["loss_function"],
            result["mae"],
            result["rmse"],
            result["mape"],
            result["training_samples"],
            result["testing_samples"]
        )
    )

    conn.commit()

    conn.close()