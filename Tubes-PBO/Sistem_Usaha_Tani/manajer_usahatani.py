# manajer_usahatani.py

import database
from model import Tanaman, BiayaProduksi, Panen


class UsahaTaniManager:
    """
    Mengelola seluruh proses bisnis Sistem Analisis
    Biaya Produksi dan Keuntungan Usaha Tani.
    """

    def __init__(self):
        """
        Inisialisasi database.
        """
        database.setup_database()

    # =====================================================
    # TANAMAN
    # =====================================================

    def tambah_tanaman(self, tanaman: Tanaman):
        """
        Menambahkan data tanaman.
        """

        try:

            if not isinstance(tanaman, Tanaman):
                raise TypeError("Objek harus bertipe Tanaman.")

            sql = """
            INSERT INTO tanaman
            (
                nama_petani,
                jenis_tanaman,
                luas_lahan,
                tanggal_tanam
            )
            VALUES (?,?,?,?)
            """

            params = (
                tanaman.nama_petani,
                tanaman.jenis_tanaman,
                tanaman.luas_lahan,
                tanaman.tanggal_tanam.strftime("%Y-%m-%d")
            )

            last_id = database.execute_query(sql, params)

            if last_id is not None:
                tanaman.id = last_id
                return True

            return False

        except Exception as e:

            print(f"Gagal menambah tanaman : {e}")

            return False

    def get_all_tanaman(self):
        """
        Mengambil seluruh data tanaman.
        """

        try:

            sql = """
            SELECT *
            FROM tanaman
            ORDER BY id DESC
            """

            rows = database.fetch_query(sql)

            data = []

            if rows:

                for row in rows:

                    data.append(

                        Tanaman(
                            nama_petani=row["nama_petani"],
                            jenis_tanaman=row["jenis_tanaman"],
                            luas_lahan=row["luas_lahan"],
                            tanggal_tanam=row["tanggal_tanam"],
                            id_tanaman=row["id"]
                        )

                    )

            return data

        except Exception as e:

            print(f"Gagal mengambil data tanaman : {e}")

            return []

    def get_tanaman_by_id(self, id_tanaman):
        """
        Mengambil tanaman berdasarkan ID.
        """

        try:

            sql = """
            SELECT *
            FROM tanaman
            WHERE id = ?
            """

            row = database.fetch_query(
                sql,
                (id_tanaman,),
                fetch_all=False
            )

            if row:

                return Tanaman(
                    nama_petani=row["nama_petani"],
                    jenis_tanaman=row["jenis_tanaman"],
                    luas_lahan=row["luas_lahan"],
                    tanggal_tanam=row["tanggal_tanam"],
                    id_tanaman=row["id"]
                )

            return None

        except Exception as e:

            print(f"Gagal mencari data tanaman : {e}")

            return None

    def update_tanaman(self, tanaman: Tanaman):
        """
        Memperbarui data tanaman.
        """

        try:

            if not isinstance(tanaman, Tanaman):
                raise TypeError("Objek harus bertipe Tanaman.")

            sql = """
            UPDATE tanaman
            SET
                nama_petani = ?,
                jenis_tanaman = ?,
                luas_lahan = ?,
                tanggal_tanam = ?
            WHERE id = ?
            """

            params = (
                tanaman.nama_petani,
                tanaman.jenis_tanaman,
                tanaman.luas_lahan,
                tanaman.tanggal_tanam.strftime("%Y-%m-%d"),
                tanaman.id
            )

            hasil = database.execute_non_query(sql, params)

            return hasil is not None

        except Exception as e:

            print(f"Gagal mengubah data tanaman : {e}")

            return False

    def hapus_tanaman(self, id_tanaman):
        """
        Menghapus data tanaman.
        """

        try:

            sql = """
            DELETE FROM tanaman
            WHERE id = ?
            """

            database.execute_non_query(sql, (id_tanaman,))

            return True

        except Exception as e:

            print(f"Gagal menghapus data tanaman : {e}")

            return False
                # =====================================================
    # BIAYA PRODUKSI
    # =====================================================

    def tambah_biaya(self, biaya: BiayaProduksi):
        """
        Menambahkan data biaya produksi.
        """

        try:

            if not isinstance(biaya, BiayaProduksi):
                raise TypeError(
                    "Objek harus bertipe BiayaProduksi."
                )

            # Pastikan tanaman tersedia
            if self.get_tanaman_by_id(biaya.tanaman_id) is None:
                raise ValueError(
                    "ID tanaman tidak ditemukan."
                )

            sql = """
            INSERT INTO biaya_produksi
            (
                tanaman_id,
                bibit,
                pupuk,
                pestisida,
                tenaga_kerja,
                sewa_alat,
                transportasi,
                lain_lain
            )
            VALUES
            (?,?,?,?,?,?,?,?)
            """

            params = (
                biaya.tanaman_id,
                biaya.bibit,
                biaya.pupuk,
                biaya.pestisida,
                biaya.tenaga_kerja,
                biaya.sewa_alat,
                biaya.transportasi,
                biaya.lain_lain
            )

            last_id = database.execute_query(sql, params)

            if last_id is not None:

                biaya.id = last_id

                return True

            return False

        except Exception as e:

            print(f"Gagal menambah biaya produksi : {e}")

            return False

    def get_all_biaya(self):
        """
        Mengambil seluruh data biaya produksi.
        """

        try:

            sql = """
            SELECT
                b.id,
                b.tanaman_id,
                t.nama_petani,
                t.jenis_tanaman,
                b.bibit,
                b.pupuk,
                b.pestisida,
                b.tenaga_kerja,
                b.sewa_alat,
                b.transportasi,
                b.lain_lain,
                (
                    b.bibit +
                    b.pupuk +
                    b.pestisida +
                    b.tenaga_kerja +
                    b.sewa_alat +
                    b.transportasi +
                    b.lain_lain
                ) AS total_biaya
            FROM biaya_produksi b
            INNER JOIN tanaman t
            ON b.tanaman_id = t.id
            ORDER BY b.id DESC
            """

            return database.get_dataframe(sql)

        except Exception as e:

            print(f"Gagal mengambil data biaya : {e}")

            return None

    def get_biaya_by_tanaman(self, tanaman_id):
        """
        Mengambil data biaya berdasarkan ID tanaman.
        """

        try:

            sql = """
            SELECT *
            FROM biaya_produksi
            WHERE tanaman_id = ?
            """

            return database.fetch_query(
                sql,
                (tanaman_id,),
                fetch_all=False
            )

        except Exception as e:

            print(f"Gagal mengambil biaya : {e}")

            return None

    def hapus_biaya(self, id_biaya):
        """
        Menghapus data biaya produksi.
        """

        try:

            sql = """
            DELETE FROM biaya_produksi
            WHERE id = ?
            """

            database.execute_query(sql, (id_biaya,))

            return True

        except Exception as e:

            print(f"Gagal menghapus biaya : {e}")

            return False
                # =====================================================
    # PANEN
    # =====================================================

    def tambah_panen(self, panen: Panen):
        """
        Menambahkan data panen.
        """

        try:

            if not isinstance(panen, Panen):
                raise TypeError(
                    "Objek harus bertipe Panen."
                )

            # Pastikan tanaman tersedia
            if self.get_tanaman_by_id(panen.tanaman_id) is None:
                raise ValueError(
                    "ID tanaman tidak ditemukan."
                )

            sql = """
            INSERT INTO panen
            (
                tanaman_id,
                hasil_panen,
                satuan,
                harga_jual,
                tanggal_panen
            )
            VALUES
            (?,?,?,?,?)
            """

            params = (
                panen.tanaman_id,
                panen.hasil_panen,
                panen.satuan,
                panen.harga_jual,
                panen.tanggal_panen.strftime("%Y-%m-%d")
            )

            last_id = database.execute_query(sql, params)

            if last_id is not None:

                panen.id = last_id

                return True

            return False

        except Exception as e:

            print(f"Gagal menambah data panen : {e}")

            return False

    def get_all_panen(self):
        """
        Mengambil seluruh data panen.
        """

        try:

            sql = """
            SELECT
                p.id,
                p.tanaman_id,
                t.nama_petani,
                t.jenis_tanaman,
                p.hasil_panen,
                p.satuan,
                p.harga_jual,
                p.tanggal_panen,
                (
                    p.hasil_panen *
                    p.harga_jual
                ) AS pendapatan
            FROM panen p
            INNER JOIN tanaman t
            ON p.tanaman_id = t.id
            ORDER BY p.id DESC
            """

            return database.get_dataframe(sql)

        except Exception as e:

            print(f"Gagal mengambil data panen : {e}")

            return None

    def get_panen_by_tanaman(self, tanaman_id):
        """
        Mengambil data panen berdasarkan ID tanaman.
        """

        try:

            sql = """
            SELECT *
            FROM panen
            WHERE tanaman_id = ?
            """

            return database.fetch_query(
                sql,
                (tanaman_id,),
                fetch_all=False
            )

        except Exception as e:

            print(f"Gagal mengambil data panen : {e}")

            return None

    def hapus_panen(self, id_panen):
        """
        Menghapus data panen.
        """

        try:

            sql = """
            DELETE FROM panen
            WHERE id = ?
            """

            database.execute_query(
                sql,
                (id_panen,)
            )

            return True

        except Exception as e:

            print(f"Gagal menghapus data panen : {e}")

            return False
                # =====================================================
    # PERHITUNGAN
    # =====================================================

    def hitung_total_biaya(self):
        """
        Menghitung total seluruh biaya produksi.
        """

        try:

            sql = """
            SELECT
            SUM(
                bibit +
                pupuk +
                pestisida +
                tenaga_kerja +
                sewa_alat +
                transportasi +
                lain_lain
            )
            AS total
            FROM biaya_produksi
            """

            hasil = database.fetch_query(
                sql,
                fetch_all=False
            )

            if hasil is None:
                return 0

            return hasil["total"] if hasil["total"] else 0

        except Exception as e:

            print(f"Gagal menghitung total biaya : {e}")

            return 0

    def hitung_total_pendapatan(self):
        """
        Menghitung total pendapatan panen.
        """

        try:

            sql = """
            SELECT
            SUM(
                hasil_panen *
                harga_jual
            )
            AS total
            FROM panen
            """

            hasil = database.fetch_query(
                sql,
                fetch_all=False
            )

            if hasil is None:
                return 0

            return hasil["total"] if hasil["total"] else 0

        except Exception as e:

            print(f"Gagal menghitung pendapatan : {e}")

            return 0

    def hitung_total_keuntungan(self):
        """
        Menghitung keuntungan bersih.
        """

        return (
            self.hitung_total_pendapatan()
            -
            self.hitung_total_biaya()
        )

    # =====================================================
    # LAPORAN
    # =====================================================

    def get_laporan(self):
        """
        Mengambil laporan lengkap usaha tani.
        """

        try:

            sql = """
            SELECT

                t.id,

                t.nama_petani,

                t.jenis_tanaman,

                t.luas_lahan,

                t.tanggal_tanam,

                IFNULL(b.bibit,0) AS bibit,

                IFNULL(b.pupuk,0) AS pupuk,

                IFNULL(b.pestisida,0) AS pestisida,

                IFNULL(b.tenaga_kerja,0) AS tenaga_kerja,

                IFNULL(b.sewa_alat,0) AS sewa_alat,

                IFNULL(b.transportasi,0) AS transportasi,

                IFNULL(b.lain_lain,0) AS lain_lain,

                (
                    IFNULL(b.bibit,0)+
                    IFNULL(b.pupuk,0)+
                    IFNULL(b.pestisida,0)+
                    IFNULL(b.tenaga_kerja,0)+
                    IFNULL(b.sewa_alat,0)+
                    IFNULL(b.transportasi,0)+
                    IFNULL(b.lain_lain,0)
                ) AS total_biaya,

                IFNULL(p.hasil_panen,0) AS hasil_panen,

                p.satuan,

                IFNULL(p.harga_jual,0) AS harga_jual,

                (
                    IFNULL(p.hasil_panen,0) *
                    IFNULL(p.harga_jual,0)
                ) AS pendapatan,

                (
                    (
                        IFNULL(p.hasil_panen,0) *
                        IFNULL(p.harga_jual,0)
                    )
                    -
                    (
                        IFNULL(b.bibit,0)+
                        IFNULL(b.pupuk,0)+
                        IFNULL(b.pestisida,0)+
                        IFNULL(b.tenaga_kerja,0)+
                        IFNULL(b.sewa_alat,0)+
                        IFNULL(b.transportasi,0)+
                        IFNULL(b.lain_lain,0)
                    )
                ) AS keuntungan

            FROM tanaman t

            LEFT JOIN biaya_produksi b
            ON t.id = b.tanaman_id

            LEFT JOIN panen p
            ON t.id = p.tanaman_id

            ORDER BY t.id DESC
            """

            return database.get_dataframe(sql)

        except Exception as e:

            print(f"Gagal mengambil laporan : {e}")

            return None
                # =====================================================
    # UTILITAS
    # =====================================================

    def jumlah_tanaman(self):
        """
        Mengembalikan jumlah seluruh data tanaman.
        """

        try:

            sql = """
            SELECT COUNT(*) AS total
            FROM tanaman
            """

            hasil = database.fetch_query(
                sql,
                fetch_all=False
            )

            if hasil:
                return hasil["total"]

            return 0

        except Exception as e:

            print(f"Gagal menghitung jumlah tanaman : {e}")

            return 0

    def jumlah_biaya(self):
        """
        Mengembalikan jumlah data biaya produksi.
        """

        try:

            sql = """
            SELECT COUNT(*) AS total
            FROM biaya_produksi
            """

            hasil = database.fetch_query(
                sql,
                fetch_all=False
            )

            if hasil:
                return hasil["total"]

            return 0

        except Exception as e:

            print(f"Gagal menghitung jumlah biaya : {e}")

            return 0

    def jumlah_panen(self):
        """
        Mengembalikan jumlah data panen.
        """

        try:

            sql = """
            SELECT COUNT(*) AS total
            FROM panen
            """

            hasil = database.fetch_query(
                sql,
                fetch_all=False
            )

            if hasil:
                return hasil["total"]

            return 0

        except Exception as e:

            print(f"Gagal menghitung jumlah panen : {e}")

            return 0

    def ringkasan(self):
        """
        Mengembalikan ringkasan sistem dalam bentuk dictionary.
        """

        return {

            "jumlah_tanaman": self.jumlah_tanaman(),

            "jumlah_biaya": self.jumlah_biaya(),

            "jumlah_panen": self.jumlah_panen(),

            "total_biaya": self.hitung_total_biaya(),

            "total_pendapatan": self.hitung_total_pendapatan(),

            "total_keuntungan": self.hitung_total_keuntungan()

        }
def jumlah_tanaman(self):
    sql = "SELECT COUNT(*) FROM tanaman"
    result = database.fetch_query(sql, fetch_all=False)

    if result and result[0]:
        return result[0]

    return 0