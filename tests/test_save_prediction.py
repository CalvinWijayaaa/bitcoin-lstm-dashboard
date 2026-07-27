from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "app"))

from predictor import get_prediction
from database import save_prediction

print("=" * 60)
print("TEST SAVE PREDICTION")
print("=" * 60)

try:
    data = get_prediction()

    save_prediction(data)

    print("✅ Prediksi berhasil disimpan ke database!")

except Exception as e:
    print("❌ Terjadi error:")
    print(e)