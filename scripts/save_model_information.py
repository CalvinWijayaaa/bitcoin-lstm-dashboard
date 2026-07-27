from datetime import datetime

from app.database import connect_db


def save_model_information():

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
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
            "LSTM",
            "BTC-USD Yahoo Finance",
            60,
            100,
            "Open, High, Low, Close, Volume",
            "Adam",
            "Mean Squared Error",

            # Ganti dengan hasil evaluasi modelmu
            0.0,     # MAE
            0.0,     # RMSE
            7.98,    # MAPE

            3445,
            862,

            datetime.now()
        )
    )

    conn.commit()
    conn.close()

    print("Model Information berhasil disimpan.")


if __name__ == "__main__":
    save_model_information()