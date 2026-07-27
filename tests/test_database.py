from pathlib import Path
import sys

# Menambahkan folder project ke Python path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "app"))

from database import connect_db


print("=" * 50)
print("TEST KONEKSI DATABASE")
print("=" * 50)

try:
    conn = connect_db()

    print("✅ Berhasil terhubung ke MySQL!")

    conn.close()

except Exception as e:

    print("❌ Gagal koneksi")

    print(e)