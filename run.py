import os

from flask import Flask

from app.routes import register_routes
from services.automation import run_pipeline

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.config["SECRET_KEY"] = "bitcoin_lstm_dashboard_2026"

print("=" * 50)
print("Template Folder :", app.template_folder)
print("Static Folder   :", app.static_folder)
print("=" * 50)

import os

try:

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        run_pipeline()

except Exception as e:

    print("=" * 60)
    print("AUTOMATION PIPELINE FAILED")
    print("=" * 60)
    print(e)
    print("Application will continue without automation.")
    print("=" * 60)
    
try:
    print("REGISTER ROUTES")
    register_routes(app)
    print("REGISTER ROUTES DONE")
except Exception as e:
    print("ERROR REGISTER ROUTES")
    print(e)
    raise

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )