# model.py

from abc import ABC, abstractmethod
import datetime


# =====================================================
# ABSTRACT CLASS
# =====================================================

class DataUsahaTani(ABC):
    @abstractmethod
    def info(self):
        pass


# =====================================================
# CLASS TANAMAN
# =====================================================

class Tanaman(DataUsahaTani):

    def __init__(
        self,
        nama_petani,
        jenis_tanaman,
        luas_lahan,
        tanggal_tanam,
        id_tanaman=None
    ):

        self.id = id_tanaman

        self.nama_petani = nama_petani
        self.jenis_tanaman = jenis_tanaman
        self.luas_lahan = luas_lahan
        self.tanggal_tanam = tanggal_tanam

    # -------------------------
    # Encapsulation
    # -------------------------

    @property
    def nama_petani(self):
        return self._nama_petani

    @nama_petani.setter
    def nama_petani(self, value):

        if not str(value).strip():
            raise ValueError("Nama petani tidak boleh kosong.")

        self._nama_petani = value.strip()

    @property
    def luas_lahan(self):
        return self._luas_lahan

    @luas_lahan.setter
    def luas_lahan(self, value):

        value = float(value)

        if value <= 0:
            raise ValueError("Luas lahan harus lebih dari nol.")

        self._luas_lahan = value

    @property
    def tanggal_tanam(self):
        return self._tanggal_tanam

    @tanggal_tanam.setter
    def tanggal_tanam(self, value):

        if isinstance(value, datetime.date):
            self._tanggal_tanam = value

        elif isinstance(value, str):
            self._tanggal_tanam = datetime.datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        else:
            raise ValueError("Format tanggal tanam tidak valid.")

    def info(self):

        return (
            f"{self.jenis_tanaman} "
            f"milik {self.nama_petani}"
        )

    def __str__(self):

        return (
            f"[{self.id}] "
            f"{self.jenis_tanaman} - "
            f"{self.nama_petani}"
        )


# CLASS BIAYA PRODUKSI

class BiayaProduksi(DataUsahaTani):

    def __init__(
        self,
        tanaman_id,
        bibit,
        pupuk,
        pestisida,
        tenaga_kerja,
        sewa_alat,
        transportasi,
        lain_lain,
        id_biaya=None
    ):

        self.id = id_biaya

        self.tanaman_id = tanaman_id

        self.bibit = float(bibit)
        self.pupuk = float(pupuk)
        self.pestisida = float(pestisida)
        self.tenaga_kerja = float(tenaga_kerja)
        self.sewa_alat = float(sewa_alat)
        self.transportasi = float(transportasi)
        self.lain_lain = float(lain_lain)

        self.validasi()

    def validasi(self):

        data = [
            self.bibit,
            self.pupuk,
            self.pestisida,
            self.tenaga_kerja,
            self.sewa_alat,
            self.transportasi,
            self.lain_lain
        ]

        for nilai in data:
            if nilai < 0:
                raise ValueError(
                    "Biaya tidak boleh bernilai negatif."
                )

    @property
    def total_biaya(self):

        return (
            self.bibit +
            self.pupuk +
            self.pestisida +
            self.tenaga_kerja +
            self.sewa_alat +
            self.transportasi +
            self.lain_lain
        )

    def info(self):

        return (
            f"Total biaya produksi : "
            f"Rp {self.total_biaya:,.0f}"
        )

    def __str__(self):

        return (
            f"Tanaman ID {self.tanaman_id} "
            f"- Rp {self.total_biaya:,.0f}"
        )

# CLASS PANEN

class Panen(DataUsahaTani):

    def __init__(
        self,
        tanaman_id,
        hasil_panen,
        satuan,
        harga_jual,
        tanggal_panen,
        id_panen=None
    ):
        self.id = id_panen
        self.tanaman_id = tanaman_id
        self.hasil_panen = float(hasil_panen)
        self.satuan = satuan
        self.harga_jual = float(harga_jual)
        self.tanggal_panen = tanggal_panen

        self.validasi()

    def validasi(self):

        if self.hasil_panen < 0:
            raise ValueError(
                "Hasil panen tidak boleh negatif."
            )

        if self.harga_jual < 0:
            raise ValueError(
                "Harga jual tidak boleh negatif."
            )

    @property
    def tanggal_panen(self):
        return self._tanggal_panen

    @tanggal_panen.setter
    def tanggal_panen(self, value):

        if isinstance(value, datetime.date):
            self._tanggal_panen = value

        elif isinstance(value, str):
            self._tanggal_panen = datetime.datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        else:
            raise ValueError("Format tanggal panen tidak valid.")

    @property
    def pendapatan(self):

        return self.hasil_panen * self.harga_jual

    def info(self):

        return (
            f"Pendapatan panen : "
            f"Rp {self.pendapatan:,.0f}"
        )

    def __str__(self):

        return (
            f"Tanaman ID {self.tanaman_id} "
            f"- Rp {self.pendapatan:,.0f}"
        )