"""
Halaman Beranda: gambaran singkat dan jalan masuk ke pemeriksaan.
"""

import streamlit as st

from services import kasus, kriteria, riwayat
from ui import tema
from ui.helper import format_vektor


def _persentase_terakhir(terakhir):
    """Mengambil persentase kasus peringkat pertama dari riwayat terakhir."""
    if terakhir is None:
        return 0.0
    detail = riwayat.detail_konsultasi(terakhir["id"])
    if len(detail) > 0:
        return detail[0]["persentase"]
    return (terakhir["cosine_tertinggi"] or 0) * 100


def _buka_menu(nama):
    """
    Callback tombol: dijalankan Streamlit sebelum widget dibuat ulang,
    sehingga aman mengubah nilai radio navigasi.
    """
    st.session_state["halaman_tujuan"] = nama


def _tampilkan_hero():
    """Area pembuka: satu ajakan jelas, satu panel ringkasan."""
    with st.container(border=True):
        kiri, kanan = st.columns([1.65, 1], gap="large")
        with kiri:
            st.markdown(
                '<div class="card-kicker">Mulai dari sini</div>'
                '<div class="hero-title">Periksa gejala, pahami kemungkinannya.</div>'
                '<p class="hero-copy">Pilih keluhan yang Anda rasakan. Sistem akan '
                "mencari kasus paling mirip dan menunjukkan rekomendasi awal "
                "beserta angka perhitungannya.</p>",
                unsafe_allow_html=True,
            )
            st.button(
                "Mulai Pemeriksaan",
                type="primary",
                on_click=_buka_menu,
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
                ])
                + "</div>",
                unsafe_allow_html=True,
            )


def _tampilkan_ringkasan(persentase):
    kol1, kol2, kol3, kol4 = st.columns(4)
    kol1.metric("Pemeriksaan tercatat", riwayat.total_konsultasi())
    kol2.metric("Kasus pembanding", kasus.total_kasus())
    kol3.metric("Gejala terdaftar", kriteria.total_kriteria())
    kol4.metric("Kemiripan terakhir", f"{round(persentase, 1)} %")


def _tampilkan_hasil_terakhir(terakhir, detail):
    with st.container(border=True):
        kol_kiri, kol_kanan = st.columns([1, 1.6], gap="large")
        with kol_kiri:
            if len(detail) > 0:
                terbaik = detail[0]
                nama_acuan = f"ID {terbaik['kasus_id']} — {terbaik['nama_kasus']}"
                keterangan = f"Cosine {round(terbaik['cosine'], 4)}"
                persentase = terbaik["persentase"]
            else:
                nama_acuan = f"ID {terakhir['kasus_acuan_id']}"
                keterangan = "Detail tidak tersedia"
                persentase = (terakhir["cosine_tertinggi"] or 0) * 100
            tema.gauge(persentase, nama_acuan, keterangan)
        with kol_kanan:
            st.markdown(
                '<div class="card-kicker">Pemeriksaan terakhir</div>',
                unsafe_allow_html=True,
            )
            tema.judul_kartu(terakhir["nama_kasus_baru"])
            st.markdown(
                tema.meta_rows([
                    ("Solusi akhir", terakhir["solusi_final"]),
                    ("Vektor input", format_vektor(terakhir["vektor_baru"])),
                    ("Dicatat", terakhir["dibuat_pada"]),
                ]),
                unsafe_allow_html=True,
            )

        if len(detail) > 0:
            st.markdown('<hr class="hairline">', unsafe_allow_html=True)
            st.write("**Tiga kasus terdekat**")
            tema.peringkas([
                {
                    "peringkat": d["peringkat"],
                    "nama": d["nama_kasus"],
                    "cosine": d["cosine"],
                    "persentase": d["persentase"],
                }
                for d in detail[:3]
            ])


def _tampilkan_riwayat_singkat():
    daftar = riwayat.daftar_konsultasi()
    if len(daftar) == 0:
        return

    baris = []
    for k in daftar[:5]:
        detail = riwayat.detail_konsultasi(k["id"])
        persentase = (
            detail[0]["persentase"]
            if detail
            else (k["cosine_tertinggi"] or 0) * 100
        )
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
        eyebrow="CEKDBD",
    )
    _tampilkan_hero()

    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    tema.quick_steps()

    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    terakhir = riwayat.konsultasi_terakhir()
    persentase = _persentase_terakhir(terakhir)
    _tampilkan_ringkasan(persentase)

    st.markdown('<hr class="hairline">', unsafe_allow_html=True)

    if terakhir is None:
        tema.bagian("01", "Hasil Terakhir", "Belum ada pemeriksaan yang tercatat.")
        tema.kosong(
            "Belum ada hasil",
            "Mulai pemeriksaan pertama untuk melihat perbandingan kasus di sini.",
            "Gunakan tombol Mulai Pemeriksaan di bagian atas halaman.",
        )
    else:
        tema.bagian("01", "Hasil Terakhir", "Ringkasan pemeriksaan paling baru.")
        _tampilkan_hasil_terakhir(
            terakhir,
            riwayat.detail_konsultasi(terakhir["id"]),
        )

    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    tema.bagian(
        "02",
        "Cara Kerja Sistem",
        "Empat tahap yang dijalankan setiap kali Anda memeriksa gejala.",
    )
    tema.flow_cards()

    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    _tampilkan_riwayat_singkat()

    if riwayat.total_konsultasi() > 0:
        st.button(
            "Lihat Semua Riwayat",
            on_click=_buka_menu,
            args=("Riwayat",),
        )
