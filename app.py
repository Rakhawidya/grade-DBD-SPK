"""
Aplikasi utama SPK berbasis Case-Based Reasoning (CBR).

Menjalankan Streamlit dengan navigasi sidebar. Seluruh perhitungan berada
di paket `core/`, seluruh akses database di paket `services/`, dan seluruh
tampilan di paket `ui/`.

Cara menjalankan:
    streamlit run app.py
"""

import streamlit as st

from services.database import inisialisasi_database
from ui import dashboard, kasus, konsultasi, kriteria, riwayat, tema

st.set_page_config(
    page_title="SPK CBR - Demam Berdarah Dengue",
    page_icon="🩺",
    layout="wide",
)

# CSS konsisten dipasang lebih awal supaya semua halaman memakai gaya yang sama.
tema.terapkan_tema()

# Pastikan tabel + data awal siap sebelum halaman mana pun dibuka.
inisialisasi_database()

st.sidebar.markdown(tema.sidebar_hero(), unsafe_allow_html=True)

HALAMAN = {
    "Dashboard": dashboard,
    "Konsultasi Baru": konsultasi,
    "Manajemen Kasus": kasus,
    "Manajemen Kriteria": kriteria,
    "Riwayat Perhitungan": riwayat,
}

pilihan = st.sidebar.radio(
    "Menu Utama",
    list(HALAMAN.keys()),
    format_func=tema.ikon_menu,
)

st.sidebar.divider()
st.sidebar.markdown(tema.sidebar_info(), unsafe_allow_html=True)
st.sidebar.caption("Versi 1.0 · Dibuat untuk pembelajaran SPK")

# --- Render halaman terpilih ---
HALAMAN[pilihan].tampilkan()
