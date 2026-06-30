# database.py

import sqlite3
import pandas as pd
from konfigurasi import DB_PATH


# =====================================================
# KONEKSI DATABASE
# =====================================================

def get_db_connection():
    """
    Membuka koneksi ke database SQLite.
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    except sqlite3.Error as e:
        print(f"Database Error : {e}")
        return None


# =====================================================
# EXECUTE QUERY
# =====================================================

def execute_query(query, params=None):
    """
    Menjalankan query INSERT, UPDATE, DELETE.
    """

    conn = get_db_connection()

    if conn is None:
        return None

    try:

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()

        return cursor.lastrowid

    except sqlite3.Error as e:

        print(f"SQLite Error : {e}")

        conn.rollback()

        return None

    finally:

        conn.close()


# =====================================================
# FETCH QUERY
# =====================================================

def fetch_query(query, params=None, fetch_all=True):
    """
    Menjalankan query SELECT.
    """

    conn = get_db_connection()

    if conn is None:
        return None

    try:

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch_all:
            return cursor.fetchall()

        return cursor.fetchone()

    except sqlite3.Error as e:

        print(f"SQLite Error : {e}")

        return None

    finally:

        conn.close()


# =====================================================
# DATAFRAME
# =====================================================

def get_dataframe(query, params=None):
    """
    Mengambil hasil query menjadi DataFrame Pandas.
    """

    conn = get_db_connection()

    if conn is None:
        return pd.DataFrame()

    try:

        return pd.read_sql_query(query, conn, params=params)

    except Exception as e:

        print(f"Pandas Error : {e}")

        return pd.DataFrame()

    finally:

        conn.close()


# =====================================================
# MEMBUAT DATABASE
# =====================================================

def setup_database():
    """
    Membuat seluruh tabel jika belum tersedia.
    """

    conn = get_db_connection()

    if conn is None:
        return False

    try:

        cursor = conn.cursor()

        # =================================================
        # TABEL TANAMAN
        # =================================================

        sql_create_tanaman = """
        CREATE TABLE IF NOT EXISTS tanaman(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nama_petani TEXT NOT NULL,

            jenis_tanaman TEXT NOT NULL,

            luas_lahan REAL NOT NULL CHECK(luas_lahan > 0),

            tanggal_tanam DATE NOT NULL

        );
        """

        cursor.execute(sql_create_tanaman)

        # =================================================
        # TABEL BIAYA PRODUKSI
        # =================================================

        sql_create_biaya = """
        CREATE TABLE IF NOT EXISTS biaya_produksi(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tanaman_id INTEGER NOT NULL,

            bibit REAL DEFAULT 0 CHECK(bibit >= 0),

            pupuk REAL DEFAULT 0 CHECK(pupuk >= 0),

            pestisida REAL DEFAULT 0 CHECK(pestisida >= 0),

            tenaga_kerja REAL DEFAULT 0 CHECK(tenaga_kerja >= 0),

            sewa_alat REAL DEFAULT 0 CHECK(sewa_alat >= 0),

            transportasi REAL DEFAULT 0 CHECK(transportasi >= 0),

            lain_lain REAL DEFAULT 0 CHECK(lain_lain >= 0),

            FOREIGN KEY(tanaman_id)
            REFERENCES tanaman(id)
            ON DELETE CASCADE

        );
        """

        cursor.execute(sql_create_biaya)

        # =================================================
        # TABEL PANEN
        # =================================================

        sql_create_panen = """
        CREATE TABLE IF NOT EXISTS panen(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tanaman_id INTEGER NOT NULL UNIQUE,

            hasil_panen REAL NOT NULL
                CHECK(hasil_panen >= 0),

            satuan TEXT NOT NULL,

            harga_jual REAL NOT NULL
                CHECK(harga_jual >= 0),

            tanggal_panen DATE NOT NULL,

            FOREIGN KEY(tanaman_id)
                REFERENCES tanaman(id)
                ON DELETE CASCADE

        );
        """

        cursor.execute(sql_create_panen)

        conn.commit()

        print("=" * 50)
        print("Database berhasil diinisialisasi.")
        print("Tabel tanaman         : OK")
        print("Tabel biaya_produksi  : OK")
        print("Tabel panen           : OK")
        print("=" * 50)

        return True

    except sqlite3.Error as e:

        print(f"Setup Database Error : {e}")

        conn.rollback()

        return False

    finally:

        conn.close()


# =====================================================
# EXECUTE NON QUERY
# =====================================================

def execute_non_query(query, params=None):
    """
    Menjalankan query UPDATE atau DELETE.

    Return:
        True  -> jika ada baris yang berubah
        False -> jika gagal atau tidak ada data yang berubah
    """

    conn = get_db_connection()

    if conn is None:
        return False

    try:

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()

        return cursor.rowcount > 0

    except sqlite3.Error as e:

        print(f"SQLite Error : {e}")

        conn.rollback()

        return False

    finally:

        conn.close()