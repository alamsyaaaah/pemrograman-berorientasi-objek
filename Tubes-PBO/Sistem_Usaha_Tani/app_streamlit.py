# =====================================================
# APP STREAMLIT
# Sistem Analisis Biaya Produksi dan Keuntungan Usaha Tani
# =====================================================

import streamlit as st
import pandas as pd
import datetime

from manajer_usahatani import UsahaTaniManager
from model import Tanaman, BiayaProduksi, Panen
from konfigurasi import JENIS_TANAMAN

# =====================================================
# INISIALISASI
# =====================================================

manager = UsahaTaniManager()

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Sistem Analisis Usaha Tani",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Sistem Analisis Biaya Produksi dan Keuntungan Usaha Tani")

st.markdown("---")

# =====================================================
# SIDEBAR
# =====================================================

menu = st.sidebar.selectbox(
    "📋 Pilih Menu",
    (
        "Dashboard",
        "Tambah Tanaman",
        "Data Tanaman",
        "Tambah Biaya",
        "Data Biaya",
        "Tambah Panen",
        "Data Panen",
        "Analisis",
        "Laporan"
    )
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    try:

        total_tanaman = manager.jumlah_tanaman()

    except Exception:

        total_tanaman = len(manager.get_all_tanaman())

    total_biaya = manager.hitung_total_biaya()
    total_pendapatan = manager.hitung_total_pendapatan()
    total_keuntungan = manager.hitung_total_keuntungan()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌱 Total Tanaman",
        total_tanaman
    )

    col2.metric(
        "💰 Total Biaya",
        f"Rp {total_biaya:,.0f}"
    )

    col3.metric(
        "📈 Pendapatan",
        f"Rp {total_pendapatan:,.0f}"
    )

    col4.metric(
        "🏆 Keuntungan",
        f"Rp {total_keuntungan:,.0f}"
    )

    st.markdown("---")

    if total_keuntungan > 0:

        st.success(
            f"Usaha memperoleh keuntungan sebesar "
            f"Rp {total_keuntungan:,.0f}"
        )

    elif total_keuntungan < 0:

        st.error(
            f"Usaha mengalami kerugian sebesar "
            f"Rp {abs(total_keuntungan):,.0f}"
        )

    else:

        st.info("Belum ada keuntungan maupun kerugian.")
        # =====================================================
# TAMBAH TANAMAN
# =====================================================

elif menu == "Tambah Tanaman":

    st.header("🌱 Tambah Data Tanaman")

    with st.form("form_tanaman"):

        nama_petani = st.text_input("Nama Petani")

        jenis_tanaman = st.selectbox(
            "Jenis Tanaman",
            JENIS_TANAMAN
        )

        luas_lahan = st.number_input(
            "Luas Lahan (Ha)",
            min_value=0.1,
            step=0.1,
            format="%.2f"
        )

        tanggal_tanam = st.date_input(
            "Tanggal Tanam",
            datetime.date.today()
        )

        simpan = st.form_submit_button("💾 Simpan")

        if simpan:

            try:

                tanaman = Tanaman(
                    nama_petani=nama_petani,
                    jenis_tanaman=jenis_tanaman,
                    luas_lahan=luas_lahan,
                    tanggal_tanam=tanggal_tanam
                )

                if manager.tambah_tanaman(tanaman):

                    st.success("Data tanaman berhasil disimpan.")

                else:

                    st.error("Data gagal disimpan.")

            except Exception as e:

                st.error(str(e))


# =====================================================
# DATA TANAMAN
# =====================================================

elif menu == "Data Tanaman":

    st.header("📋 Data Tanaman")

    data = manager.get_all_tanaman()

    if len(data) == 0:

        st.info("Belum ada data tanaman.")

    else:

        tabel = []

        for t in data:

            tabel.append({

                "ID": t.id,

                "Nama Petani": t.nama_petani,

                "Jenis Tanaman": t.jenis_tanaman,

                "Luas Lahan (Ha)": t.luas_lahan,

                "Tanggal Tanam": t.tanggal_tanam

            })

        df = pd.DataFrame(tabel)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Total Data : {len(df)} tanaman"
        )
        # =====================================================
# TAMBAH BIAYA PRODUKSI
# =====================================================

elif menu == "Tambah Biaya":

    st.header("💰 Tambah Biaya Produksi")

    daftar_tanaman = manager.get_all_tanaman()

    if len(daftar_tanaman) == 0:

        st.warning("Belum ada data tanaman. Silakan tambah data tanaman terlebih dahulu.")

    else:

        pilihan = {
            f"{t.id} - {t.nama_petani} ({t.jenis_tanaman})": t.id
            for t in daftar_tanaman
        }

        with st.form("form_biaya"):

            tanaman = st.selectbox(
                "Pilih Tanaman",
                list(pilihan.keys())
            )

            bibit = st.number_input(
                "Biaya Bibit",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            pupuk = st.number_input(
                "Biaya Pupuk",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            pestisida = st.number_input(
                "Biaya Pestisida",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            tenaga = st.number_input(
                "Biaya Tenaga Kerja",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            sewa = st.number_input(
                "Biaya Sewa Alat",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            transport = st.number_input(
                "Biaya Transportasi",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            lain = st.number_input(
                "Biaya Lain-lain",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            simpan = st.form_submit_button("💾 Simpan Biaya")

            if simpan:

                try:

                    biaya = BiayaProduksi(
                        tanaman_id=pilihan[tanaman],
                        bibit=bibit,
                        pupuk=pupuk,
                        pestisida=pestisida,
                        tenaga_kerja=tenaga,
                        sewa_alat=sewa,
                        transportasi=transport,
                        lain_lain=lain
                    )

                    if manager.tambah_biaya(biaya):

                        st.success("Data biaya berhasil disimpan.")

                    else:

                        st.error("Data biaya gagal disimpan.")

                except Exception as e:

                    st.error(str(e))


# =====================================================
# DATA BIAYA PRODUKSI
# =====================================================

elif menu == "Data Biaya":

    st.header("📊 Data Biaya Produksi")

    df = manager.get_all_biaya()

    if df.empty:

        st.info("Belum ada data biaya produksi.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Total Data : {len(df)} biaya produksi"
        )
        # =====================================================
# TAMBAH DATA PANEN
# =====================================================

elif menu == "Tambah Panen":

    st.header("🌾 Tambah Data Panen")

    daftar_tanaman = manager.get_all_tanaman()

    if len(daftar_tanaman) == 0:

        st.warning("Belum ada data tanaman.")

    else:

        pilihan = {
            f"{t.id} - {t.nama_petani} ({t.jenis_tanaman})": t.id
            for t in daftar_tanaman
        }

        with st.form("form_panen"):

            tanaman = st.selectbox(
                "Pilih Tanaman",
                list(pilihan.keys())
            )

            hasil_panen = st.number_input(
                "Hasil Panen",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

            satuan = st.selectbox(
                "Satuan",
                [
                    "Kg",
                    "Ton",
                    "Karung",
                    "Kwintal"
                ]
            )

            harga_jual = st.number_input(
                "Harga Jual per Satuan (Rp)",
                min_value=0.0,
                value=0.0,
                step=1000.0
            )

            tanggal_panen = st.date_input(
                "Tanggal Panen",
                datetime.date.today()
            )

            simpan = st.form_submit_button("💾 Simpan Panen")

            if simpan:

                try:

                    panen = Panen(
                        tanaman_id=pilihan[tanaman],
                        hasil_panen=hasil_panen,
                        satuan=satuan,
                        harga_jual=harga_jual,
                        tanggal_panen=tanggal_panen
                    )

                    if manager.tambah_panen(panen):

                        st.success("Data panen berhasil disimpan.")

                    else:

                        st.error("Data panen gagal disimpan.")

                except Exception as e:

                    st.error(str(e))


# =====================================================
# DATA PANEN
# =====================================================

elif menu == "Data Panen":

    st.header("📦 Data Panen")

    df = manager.get_all_panen()

    if df.empty:

        st.info("Belum ada data panen.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Total Data : {len(df)} data panen"
        )
        # =====================================================
# ANALISIS USAHA TANI
# =====================================================

elif menu == "Analisis":

    st.header("📈 Analisis Usaha Tani")

    total_biaya = manager.hitung_total_biaya()
    total_pendapatan = manager.hitung_total_pendapatan()
    total_keuntungan = manager.hitung_total_keuntungan()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Total Biaya Produksi",
            f"Rp {total_biaya:,.0f}"
        )

    with col2:
        st.metric(
            "📈 Total Pendapatan",
            f"Rp {total_pendapatan:,.0f}"
        )

    with col3:
        st.metric(
            "🏆 Total Keuntungan",
            f"Rp {total_keuntungan:,.0f}"
        )

    st.divider()

    if total_keuntungan > 0:

        st.success(
            f"Usaha tani memperoleh keuntungan sebesar "
            f"Rp {total_keuntungan:,.0f}"
        )

    elif total_keuntungan < 0:

        st.error(
            f"Usaha tani mengalami kerugian sebesar "
            f"Rp {abs(total_keuntungan):,.0f}"
        )

    else:

        st.warning(
            "Belum terdapat keuntungan maupun kerugian."
        )


# =====================================================
# LAPORAN LENGKAP
# =====================================================

elif menu == "Laporan":

    st.header("📄 Laporan Lengkap Usaha Tani")

    df = manager.get_laporan()

    if df.empty:

        st.info("Belum ada data laporan.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="📥 Download Laporan CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="laporan_usaha_tani.csv",
            mime="text/csv"
        )

        st.success(
            f"Jumlah Data Laporan : {len(df)}"
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Sistem Analisis Biaya Produksi dan Keuntungan Usaha Tani | "
    "Pemrograman Berorientasi Objek (Python + SQLite + Streamlit)"
)