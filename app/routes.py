import pandas as pd
from pathlib import Path
from flask import (
    render_template,
    redirect,
    url_for,
    flash
)


from app.predictor import get_prediction

from app.database import (
    get_latest_prediction,
    get_prediction_history,
    get_model_information,
    get_prediction_result,
    save_prediction
)


def register_routes(app):

    @app.route("/")
    def dashboard():

        # ==========================
        # DATABASE
        # ==========================

        try:

            data = get_latest_prediction()

            history = get_prediction_history()

            model = get_model_information()

            actual_price, predicted_price = get_prediction_result()

            database_status = True

        except Exception as e:

            print(f"Database Error: {e}")

            data = None
            history = []
            model = None
            actual_price = []
            predicted_price = []

            database_status = False
        
        # ==========================
        # SYSTEM STATUS
        # ==========================

        from pathlib import Path

        BASE_DIR = Path(__file__).resolve().parent.parent

        dataset_status = (
            BASE_DIR / "dataset" / "raw" / "btc_usd_yahoo_daily_full.csv"
        ).exists()

        model_status = (
            BASE_DIR / "models" / "bitcoin_lstm.keras"
        ).exists()

        prediction_status = data is not None
        
        # ==========================
        # DATA HISTORICAL BITCOIN
        # ==========================

        csv_path = (
        Path(__file__).parent.parent
        / "dataset"
        / "raw"
        / "btc_usd_yahoo_daily_full.csv"
    )

        # ==========================
        # CHART DATA
        # ==========================

        chart_labels = []

        chart_prices = []

        try:

            df = pd.read_csv(csv_path)

            last60 = df.tail(60)

            chart_labels = last60["Date"].tolist()

            chart_prices = last60["Close"].tolist()

            chart_labels.append("Tomorrow")

            if data:

                chart_prices.append(data["predicted_price"])

            else:

                chart_prices.append(None)

        except Exception:

            chart_labels = []

            chart_prices = []

        return render_template(
            "dashboard.html",
            data=data,
            history=history,
            model=model,
            chart_prices=chart_prices,
            actual_price=actual_price,
            predicted_price=predicted_price,

            dataset_status=dataset_status,
            model_status=model_status,
            database_status=database_status,
            prediction_status=prediction_status,
        )

    @app.route("/about")
    def about():

        return render_template("about.html")
        
    @app.route("/predict", methods=["POST"])
    def predict_latest():

        print("=" * 60)
        print("MANUAL PREDICTION")
        print("=" * 60)

        try:

            prediction = get_prediction()

            save_prediction(prediction)

            flash(
                "Prediction completed successfully.",
                "success"
            )

        except Exception as e:

            import traceback
            traceback.print_exc()

            flash(
                str(e),
                "danger"
            )

        return redirect(url_for("dashboard"))