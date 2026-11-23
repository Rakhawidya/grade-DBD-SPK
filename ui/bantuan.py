"""
Helper UI kecil yang dipakai lebih dari satu halaman.

Modul ini sengaja hanya berisi perakitan tampilan dan callback navigasi.
Semua perhitungan tetap berada di `core/`, semua akses data tetap lewat
`services/`, dan urutan pembuatan widget di halaman tidak diubah.
"""

import streamlit as st

from ui import tema


def panel_meta(baris, gelap=False):
    """Merender daftar pasangan label/nilai sebagai HTML meta rows."""
    st.markdown(tema.meta_rows(baris, gelap=gelap), unsafe_allow_html=True)


def peringkas_dari_hasil(hasil, batas=3, kunci_nama="nama"):
    """Membentuk ringkasan 3 kasus teratas dari hasil retrieve/rekaman."""
    return [
        {
            "peringkat": h["peringkat"],
            "nama": h[kunci_nama],
            "cosine": h["cosine"],
            "persentase": h["persentase"],
        }
        for h in hasil[:batas]
    ]


def persentase_dari_catatan(catatan, detail):
    """
    Mengambil persentase dan nama kasus acuan dari satu catatan riwayat.

    Detail perbandingan dipakai bila tersedia; bila tidak, keduanya diambil
    dari kolom ringkasan. Logika ini sebelumnya ditulis ulang di Beranda
    dan Riwayat.
    """
    if len(detail) > 0:
        terbaik = detail[0]
        return (
            terbaik["persentase"],
            f"ID {terbaik['kasus_id']} — {terbaik['nama_kasus']}",
        )
    return (
        (catatan["cosine_tertinggi"] or 0) * 100,
        f"ID {catatan['kasus_acuan_id']}",
    )


def buka_menu(nama):
    """Callback tombol: menulis halaman tujuan sebelum widget dibuat ulang."""
    st.session_state["halaman_tujuan"] = nama
