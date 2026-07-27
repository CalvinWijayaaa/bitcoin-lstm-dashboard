from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT / "app"))

from database import get_latest_prediction

print("="*60)
print("LATEST PREDICTION")
print("="*60)

data = get_latest_prediction()

print(data)