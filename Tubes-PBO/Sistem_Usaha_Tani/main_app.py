# =====================================================
# main_app.py
# Sistem Analisis Biaya Produksi dan
# Keuntungan Usaha Tani
# =====================================================

import os
import datetime

import pandas as pd

from model import Tanaman, BiayaProduksi, Panen
from manajer_usahatani import UsahaTaniManager
from konfigurasi import JENIS_TANAMAN


# =====================================================
# INISIALISASI
# =====================================================

manager = UsahaTaniManager()


# =====================================================
# UTILITAS
# =====================================================

def clear_screen():
    """
    Membersihkan layar terminal.
    """

    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """
    Menunggu input pengguna.
    """

    input("\nTekan ENTER untuk melanjutkan...")


def tampil_header():
    """
    Menampilkan judul aplikasi.
    """

    clear_screen()

    print("=" * 70)
    print(" SISTEM ANALISIS BIAYA PRODUKSI DAN KEUNTUNGAN USAHA TANI ")
    print("=" * 70)


def input_float(pesan):
    """
    Input angka desimal.
    """

    while True:

        try:

            nilai = float(input(pesan))

            if nilai < 0:
                print("Input tidak boleh negatif.")
                continue

            return nilai

        except ValueError:

            print("Masukkan angka yang benar.")


def input_tanggal(pesan):
    """
    Input tanggal format YYYY-MM-DD.
    """

    while True:

        tanggal = input(pesan)

        try:

            return datetime.datetime.strptime(
                tanggal,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            print("Format tanggal salah.")
            print("Gunakan format : YYYY-MM-DD")


def pilih_tanaman():
    """
    Menampilkan daftar tanaman lalu
    meminta pengguna memilih ID.
    """

    data = manager.get_all_tanaman()

    if len(data) == 0:

        print("\nBelum ada data tanaman.")

        return None

    print("\nDAFTAR TANAMAN")
    print("-" * 70)

    for tanaman in data:

        print(
            f"{tanaman.id}. "
            f"{tanaman.nama_petani}"
            f" | {tanaman.jenis_tanaman}"
            f" | {tanaman.luas_lahan} Ha"
        )

    print("-" * 70)

    while True:

        try:

            id_tanaman = int(
                input("Masukkan ID Tanaman : ")
            )

            tanaman = manager.get_tanaman_by_id(
                id_tanaman
            )

            if tanaman is None:

                print("ID tidak ditemukan.")

                continue

            return tanaman

        except ValueError:

            print("Masukkan angka yang benar.")


def tampil_dataframe(df, judul):
    """
    Menampilkan DataFrame dengan rapi.
    """

    print("\n" + "=" * 70)
    print(judul.upper())
    print("=" * 70)

    if df is None:
        print("Data tidak tersedia.")
        return

    if isinstance(df, pd.DataFrame):

        if df.empty:
            print("Belum ada data.")
        else:
            print(df.to_string(index=False))

    else:
        print(df)


# =====================================================
# MENU
# =====================================================
# =====================================================
# MENU TAMBAH TANAMAN
# =====================================================

def menu_tambah_tanaman():
    """
    Menu untuk menambahkan data tanaman.
    """

    tampil_header()

    print("TAMBAH DATA TANAMAN")
    print("-" * 70)

    try:

        nama_petani = input(
            "Nama Petani            : "
        ).strip()

        print("\nJenis Tanaman")

        for i, jenis in enumerate(JENIS_TANAMAN, start=1):
            print(f"{i}. {jenis}")

        while True:

            try:

                pilihan = int(
                    input("Pilih Jenis Tanaman : ")
                )

                if 1 <= pilihan <= len(JENIS_TANAMAN):
                    jenis_tanaman = JENIS_TANAMAN[
                        pilihan - 1
                    ]
                    break

                print("Pilihan tidak tersedia.")

            except ValueError:

                print("Masukkan angka yang benar.")

        luas_lahan = input_float(
            "Luas Lahan (Ha)       : "
        )

        tanggal_tanam = input_tanggal(
            "Tanggal Tanam (YYYY-MM-DD) : "
        )

        tanaman = Tanaman(
            nama_petani=nama_petani,
            jenis_tanaman=jenis_tanaman,
            luas_lahan=luas_lahan,
            tanggal_tanam=tanggal_tanam
        )

        if manager.tambah_tanaman(tanaman):

            print("\nData tanaman berhasil disimpan.")

        else:

            print("\nGagal menyimpan data tanaman.")

    except Exception as e:

        print(f"\nTerjadi kesalahan : {e}")

    pause()


# =====================================================
# MENU LIHAT DATA TANAMAN
# =====================================================

def menu_data_tanaman():
    """
    Menampilkan seluruh data tanaman.
    """

    tampil_header()

    data = manager.get_all_tanaman()

    if len(data) == 0:

        print("Belum ada data tanaman.")

        pause()

        return

    rows = []

    for t in data:

        rows.append({

            "ID": t.id,

            "Nama Petani": t.nama_petani,

            "Jenis Tanaman": t.jenis_tanaman,

            "Luas Lahan": t.luas_lahan,

            "Tanggal Tanam":
                t.tanggal_tanam.strftime("%Y-%m-%d")

        })

    df = pd.DataFrame(rows)

    tampil_dataframe(
        df,
        "DATA TANAMAN"
    )

    pause()
    # =====================================================
# MENU BIAYA PRODUKSI
# =====================================================

def menu_tambah_biaya():
    """
    Menu untuk menambahkan biaya produksi.
    """

    tampil_header()

    print("TAMBAH BIAYA PRODUKSI")
    print("-" * 70)

    tanaman = pilih_tanaman()

    if tanaman is None:

        pause()

        return

    try:

        print(f"\nPetani          : {tanaman.nama_petani}")
        print(f"Jenis Tanaman   : {tanaman.jenis_tanaman}")

        print("\nMasukkan seluruh biaya produksi")

        bibit = input_float("Biaya Bibit          : Rp ")
        pupuk = input_float("Biaya Pupuk          : Rp ")
        pestisida = input_float("Biaya Pestisida      : Rp ")
        tenaga_kerja = input_float("Biaya Tenaga Kerja   : Rp ")
        sewa_alat = input_float("Biaya Sewa Alat      : Rp ")
        transportasi = input_float("Biaya Transportasi   : Rp ")
        lain_lain = input_float("Biaya Lain-lain      : Rp ")

        biaya = BiayaProduksi(

            tanaman_id=tanaman.id,

            bibit=bibit,

            pupuk=pupuk,

            pestisida=pestisida,

            tenaga_kerja=tenaga_kerja,

            sewa_alat=sewa_alat,

            transportasi=transportasi,

            lain_lain=lain_lain

        )

        if manager.tambah_biaya(biaya):

            print("\nData biaya produksi berhasil disimpan.")

            print(f"Total Biaya : Rp {biaya.total_biaya:,.0f}")

        else:

            print("\nGagal menyimpan biaya produksi.")

    except Exception as e:

        print(f"\nTerjadi kesalahan : {e}")

    pause()


# =====================================================
# MENU DATA BIAYA PRODUKSI
# =====================================================

def menu_data_biaya():
    """
    Menampilkan seluruh data biaya produksi.
    """

    tampil_header()

    df = manager.get_all_biaya()

    tampil_dataframe(
        df,
        "DATA BIAYA PRODUKSI"
    )

    pause()
    # =====================================================
# MENU PANEN
# =====================================================

def menu_tambah_panen():
    """
    Menu untuk menambahkan data panen.
    """

    tampil_header()

    print("TAMBAH DATA PANEN")
    print("-" * 70)

    tanaman = pilih_tanaman()

    if tanaman is None:

        pause()

        return

    try:

        print(f"\nPetani         : {tanaman.nama_petani}")
        print(f"Jenis Tanaman  : {tanaman.jenis_tanaman}")

        hasil_panen = input_float(
            "\nHasil Panen : "
        )

        satuan = input(
            "Satuan (Kg/Ton/Karung) : "
        ).strip()

        harga_jual = input_float(
            "Harga Jual per Satuan : Rp "
        )

        tanggal_panen = input_tanggal(
            "Tanggal Panen (YYYY-MM-DD) : "
        )

        panen = Panen(

            tanaman_id=tanaman.id,

            hasil_panen=hasil_panen,

            satuan=satuan,

            harga_jual=harga_jual,

            tanggal_panen=tanggal_panen

        )

        if manager.tambah_panen(panen):

            print("\nData panen berhasil disimpan.")

            print(
                f"Pendapatan : "
                f"Rp {panen.pendapatan:,.0f}"
            )

        else:

            print("\nGagal menyimpan data panen.")

    except Exception as e:

        print(f"\nTerjadi kesalahan : {e}")

    pause()


# =====================================================
# MENU DATA PANEN
# =====================================================

def menu_data_panen():
    """
    Menampilkan seluruh data panen.
    """

    tampil_header()

    df = manager.get_all_panen()

    tampil_dataframe(
        df,
        "DATA PANEN"
    )

    pause()
    # =====================================================
# MENU ANALISIS
# =====================================================

def menu_analisis():
    """
    Menampilkan hasil analisis usaha tani.
    """

    tampil_header()

    print("ANALISIS BIAYA PRODUKSI DAN KEUNTUNGAN")
    print("=" * 70)

    total_biaya = manager.hitung_total_biaya()
    total_pendapatan = manager.hitung_total_pendapatan()
    total_keuntungan = manager.hitung_total_keuntungan()

    print(f"\nTotal Biaya Produksi : Rp {total_biaya:,.0f}")
    print(f"Total Pendapatan     : Rp {total_pendapatan:,.0f}")
    print(f"Total Keuntungan     : Rp {total_keuntungan:,.0f}")

    print("\n" + "=" * 70)

    if total_keuntungan > 0:

        print("Status Usaha : UNTUNG")

    elif total_keuntungan < 0:

        print("Status Usaha : RUGI")

    else:

        print("Status Usaha : IMPAS")

    pause()


# =====================================================
# MENU RINGKASAN
# =====================================================

def menu_ringkasan():
    """
    Menampilkan ringkasan data sistem.
    """

    tampil_header()

    data = manager.ringkasan()

    print("RINGKASAN SISTEM")
    print("=" * 70)

    print(f"Jumlah Tanaman    : {data['jumlah_tanaman']}")
    print(f"Jumlah Data Biaya : {data['jumlah_biaya']}")
    print(f"Jumlah Data Panen : {data['jumlah_panen']}")

    print("-" * 70)

    print(f"Total Biaya       : Rp {data['total_biaya']:,.0f}")
    print(f"Total Pendapatan  : Rp {data['total_pendapatan']:,.0f}")
    print(f"Total Keuntungan  : Rp {data['total_keuntungan']:,.0f}")

    pause()


# =====================================================
# MENU LAPORAN
# =====================================================

def menu_laporan():
    """
    Menampilkan laporan lengkap usaha tani.
    """

    tampil_header()

    df = manager.get_laporan()

    tampil_dataframe(
        df,
        "LAPORAN USAHA TANI"
    )

    pause()
    # =====================================================
# MENU UTAMA
# =====================================================

def menu_utama():
    """
    Menu utama aplikasi.
    """

    while True:

        tampil_header()

        print("MENU UTAMA")
        print("=" * 70)

        print("1. Tambah Data Tanaman")
        print("2. Lihat Data Tanaman")

        print()

        print("3. Tambah Biaya Produksi")
        print("4. Lihat Data Biaya Produksi")

        print()

        print("5. Tambah Data Panen")
        print("6. Lihat Data Panen")

        print()

        print("7. Analisis Usaha Tani")
        print("8. Ringkasan Sistem")
        print("9. Laporan Lengkap")

        print()

        print("0. Keluar")

        print("=" * 70)

        pilihan = input("Pilih Menu : ").strip()

        if pilihan == "1":

            menu_tambah_tanaman()

        elif pilihan == "2":

            menu_data_tanaman()

        elif pilihan == "3":

            menu_tambah_biaya()

        elif pilihan == "4":

            menu_data_biaya()

        elif pilihan == "5":

            menu_tambah_panen()

        elif pilihan == "6":

            menu_data_panen()

        elif pilihan == "7":

            menu_analisis()

        elif pilihan == "8":

            menu_ringkasan()

        elif pilihan == "9":

            menu_laporan()

        elif pilihan == "0":

            tampil_header()

            print("Terima kasih telah menggunakan aplikasi.")
            print("Sistem Analisis Biaya Produksi")
            print("dan Keuntungan Usaha Tani.")

            break

        else:

            print("\nPilihan tidak tersedia.")

            pause()


# =====================================================
# PROGRAM UTAMA
# =====================================================

if __name__ == "__main__":

    menu_utama()