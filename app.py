"""
CEKDBD — aplikasi Streamlit untuk pemeriksaan gejala berbasis kasus.

Struktur tetap dipisah:
    core/      perhitungan manual (Cosine Similarity dan tahap CBR)
    services/  database SQLite dan validasi
    ui/        seluruh tampilan

Cara menjalankan:
    streamlit run app.py
"""

import streamlit as st

from services.database import inisialisasi_database
from ui import dashboard, konsultasi, riwayat, tema

st.set_page_config(
    page_title="CEKDBD — Sistem untuk mendeteksi gejala anda",
    page_icon="assets/favicon.svg",
    layout="wide",
)

tema.terapkan_tema()
inisialisasi_database()

st.sidebar.markdown(tema.sidebar_hero(), unsafe_allow_html=True)

HALAMAN = {
    "Beranda": dashboard,
    "Cek Gejala": konsultasi,
    "Riwayat": riwayat,
}

pilihan = st.sidebar.radio(
    "Navigasi",
    list(HALAMAN.keys()),
    format_func=tema.label_menu,
    key="halaman_tujuan",
)

st.sidebar.markdown(tema.sidebar_info(), unsafe_allow_html=True)

HALAMAN[pilihan].tampilkan()
tema.footer()
