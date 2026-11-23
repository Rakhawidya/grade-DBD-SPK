"""
Halaman Beranda: gambaran singkat dan jalan masuk ke pemeriksaan.
"""

import streamlit as st

from services import kasus, kriteria, riwayat
from ui import bantuan, tema
from ui.helper import format_vektor


def _persentase_terakhir(terakhir):
    """Mengambil persentase kasus peringkat pertama dari riwayat terakhir."""
    if terakhir is None:
        return 0.0
    detail = riwayat.detail_konsultasi(terakhir["id"])
    if len(detail) > 0:
        return detail[0]["persentase"]
    return (terakhir["cosine_tertinggi"] or 0) * 100


def _tampilkan_hero():
    """Area pembuka: satu ajakan jelas, satu panel ringkasan."""
    with st.container(border=True):
        kiri, kanan = st.columns([1, 1], gap="large")
        with kiri:
            tema.kicker("Mulai dari sini")
            st.markdown(
                '<div class="hero-title">Periksa gejala, pahami kemungkinannya.</div>'
                '<p class="hero-copy">Pilih keluhan yang Anda rasakan. Sistem akan '
                "mencari kasus paling mirip dan menunjukkan rekomendasi awal "
                "beserta angka perhitungannya.</p>",
                unsafe_allow_html=True,
            )
            st.button(
                "Mulai Pemeriksaan",
                type="primary",
                on_click=bantuan.buka_menu,
                args=("Cek Gejala",),
            )
            st.caption("Berlangsung langsung di aplikasi ini, tanpa pendaftaran.")
        with kanan:
            st.markdown(
                '<div class="hero-aside">'
                '<div class="card-kicker">Ringkasan sistem</div>'
                + tema.meta_rows([
                    ("Gejala terdaftar", kriteria.total_kriteria()),
                    ("Kasus pembanding", kasus.total_kasus()),
                    ("Pemeriksaan tercatat", riwayat.total_konsultasi()),
                    ("Metode", "Cosine Similarity manual"),
                ], gelap=True)
                + "</div>",
                unsafe_allow_html=True,
            )


def _tampilkan_ringkasan(terakhir, persentase):
    nilai_terakhir = "—" if terakhir is None else f"{round(persentase, 1)} %"
    tema.stat_strip([
        ("Pemeriksaan tercatat", riwayat.total_konsultasi(), "catatan tersimpan"),
        ("Kasus pembanding", kasus.total_kasus(), "kasus pembanding aktif"),
        ("Gejala terdaftar", kriteria.total_kriteria(), "gejala yang dapat dipilih"),
        ("Kemiripan terakhir", nilai_terakhir, "dari pemeriksaan terbaru"),
    ])


def _tampilkan_hasil_terakhir(terakhir, detail):
    # Panel hanya berisi dua kolom supaya ukurannya sama dengan panel lain.
    # Ringkasan peringkat diletakkan di bawah panel, bukan di dalamnya.
    with st.container(border=True):
        kol_kiri, kol_kanan = st.columns([1, 1], gap="large")
        with kol_kiri:
            persentase, nama_acuan = bantuan.persentase_dari_catatan(terakhir, detail)
            if len(detail) > 0:
                keterangan = f"Cosine {round(detail[0]['cosine'], 4)}"
            else:
                keterangan = "Detail tidak tersedia"
            tema.gauge(persentase, nama_acuan, keterangan)
        with kol_kanan:
            tema.kicker("Pemeriksaan terakhir")
            tema.judul_kartu(terakhir["nama_kasus_baru"])
            bantuan.panel_meta([
                ("Solusi akhir", terakhir["solusi_final"]),
                ("Vektor input", format_vektor(terakhir["vektor_baru"])),
                ("Dicatat", terakhir["dibuat_pada"]),
            ])

    if len(detail) > 0:
        tema.pemisah()
        tema.kicker("Tiga kasus terdekat")
        tema.peringkas(bantuan.peringkas_dari_hasil(detail, kunci_nama="nama_kasus"))


def _tampilkan_riwayat_singkat():
    daftar = riwayat.daftar_konsultasi()
    if len(daftar) == 0:
        return

    baris = []
    for k in daftar[:5]:
        detail = riwayat.detail_konsultasi(k["id"])
        persentase = bantuan.persentase_dari_catatan(k, detail)[0]
        baris.append({
            "id": k["id"],
            "nama": k["nama_kasus_baru"],
            "solusi": k["solusi_final"],
            "waktu": k["dibuat_pada"],
            "persentase": persentase,
        })

    tema.bagian("03", "Aktivitas Terbaru", "Lima pemeriksaan terakhir.")
    with st.container(border=True):
        tema.aktivitas_ringkas(baris)


def tampilkan():
    tema.header(
        "Beranda",
        "Periksa gejala berdasarkan kasus yang sudah tercatat. Mulai pemeriksaan "
        "baru atau lihat hasil sebelumnya.",
        eyebrow="Ringkasan sistem",
    )
    _tampilkan_hero()

    tema.pemisah()
    tema.quick_steps()

    tema.pemisah()
    terakhir = riwayat.konsultasi_terakhir()
    persentase = _persentase_terakhir(terakhir)
    _tampilkan_ringkasan(terakhir, persentase)

    tema.pemisah()

    if terakhir is None:
        tema.bagian("01", "Hasil Terakhir", "Belum ada pemeriksaan yang tercatat.")
        tema.kosong(
            "Belum ada hasil",
            "Mulai pemeriksaan pertama untuk melihat perbandingan kasus di sini.",
        )
        st.button(
            "Mulai Pemeriksaan",
            key="mulai_dari_hasil_kosong",
            type="primary",
            on_click=bantuan.buka_menu,
            args=("Cek Gejala",),
        )
    else:
        tema.bagian("01", "Hasil Terakhir", "Ringkasan pemeriksaan paling baru.")
        _tampilkan_hasil_terakhir(
            terakhir,
            riwayat.detail_konsultasi(terakhir["id"]),
        )

    tema.pemisah()
    tema.bagian(
        "02",
        "Cara Kerja Sistem",
        "Empat tahap yang dijalankan setiap kali Anda memeriksa gejala.",
    )
    tema.flow_cards()

    tema.pemisah()
    _tampilkan_riwayat_singkat()

    if riwayat.total_konsultasi() > 0:
        st.button(
            "Lihat Semua Riwayat",
            on_click=bantuan.buka_menu,
            args=("Riwayat",),
        )
