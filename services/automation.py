from scripts.download_data import download_latest_data
from scripts.preprocessing import preprocess_data

from app.predictor import get_prediction
from app.database import (
    save_prediction,
    has_prediction_today
)


def run_pipeline(force=False):

    print("=" * 60)
    print("BITCOIN AUTOMATION PIPELINE")
    print("=" * 60)

    # ==================================================
    # STEP 1
    # ==================================================

    updated = download_latest_data()

    if not updated:

        print("\nTidak ada data baru.")

        has_prediction = has_prediction_today()

        print("HAS PREDICTION =", has_prediction)

        if has_prediction and not force:

            print("Prediksi hari ini sudah tersedia.")
            print("Pipeline selesai.")
            return

        print("Belum ada prediksi hari ini.")
        print("Melanjutkan proses prediksi...")

    # ==================================================
    # STEP 3
    # ==================================================

    print("\nMenjalankan prediksi...")

    prediction = get_prediction()

    save_prediction(prediction)

    print("\nHASIL PREDIKSI")

    for key, value in prediction.items():

        print(f"{key} : {value}")

    print("\nPipeline selesai.")