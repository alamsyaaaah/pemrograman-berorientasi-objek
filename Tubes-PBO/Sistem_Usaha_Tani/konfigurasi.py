# konfigurasi.py
import os
# DATABASE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = "usaha_tani.db"
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)
# DATA MASTER
JENIS_TANAMAN = [
    "Padi",
    "Jagung",
    "Cabai",
    "Tembakau"
]