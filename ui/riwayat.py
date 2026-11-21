"""
Halaman Riwayat: arsip pemeriksaan dan rincian angka yang pernah dihitung.
"""

import csv
import io

import streamlit as st

from services import riwayat as svc_riwayat
from ui import tema
from ui.helper import format_vektor


def _tampilkan_ringkasan(daftar):
    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        tema.kartu_ringkas(
            "Pemeriksaan",
            svc_riwayat.total_konsultasi(),
            "catatan yang tersimpan",
        )
    with kol2:
        tema.kartu_ringkas(
            "Perbandingan",
            svc_riwayat.total_perbandingan(),
            "baris perhitungan kasus",
        )
    with kol3:
        tema.kartu_ringkas(
            "Ditampilkan",
            len(daftar),
            "pemeriksaan dalam daftar",
        )


def _csv_ringkasan(daftar):
    """Menyusun ringkasan riwayat sebagai CSV UTF-8 yang rapi dibaca Excel."""
    keluaran = io.StringIO()
    penulis = csv.writer(keluaran)
    penulis.writerow(["ID", "Pasien", "Solusi akhir", "Cosine tertinggi", "Waktu"])
    for k in daftar:
        penulis.writerow([
            k["id"],
            k["nama_kasus_baru"],
            k["solusi_final"],
            round(k["cosine_tertinggi"] or 0, 4),
            k["dibuat_pada"],
        ])
    return keluaran.getvalue().encode("utf-8-sig")


def tampilkan():
    tema.header(
        "Riwayat",
        "Catatan pemeriksaan sebelumnya beserta angka perbandingan yang digunakan.",
        eyebrow="Arsip pemeriksaan",
    )
    semua = svc_riwayat.daftar_konsultasi()
    if len(semua) == 0:
        _tampilkan_ringkasan([])
        tema.kosong(
            "Belum ada pemeriksaan",
            "Catatan pemeriksaan akan muncul di sini setelah Anda menyimpan hasil.",
            "Buka menu 02 Cek Gejala untuk memulai pemeriksaan pertama.",
        )
        return

    with st.container(border=True):
        kol_cari, kol_aksi = st.columns([2, 1], gap="large")
        with kol_cari:
            query = st.text_input(
                "Cari pemeriksaan",
                placeholder="Nama, ID, atau solusi",
            ).strip().lower()
            st.caption("Kosongkan kolom ini untuk menampilkan semua pemeriksaan.")

        daftar = semua
        if query:
            daftar = [
                k for k in semua
                if query in str(k["id"]).lower()
                or query in str(k["nama_kasus_baru"]).lower()
                or query in str(k["solusi_final"]).lower()
            ]

        with kol_aksi:
            st.markdown(
                '<div class="card-kicker">Ekspor data</div>',
                unsafe_allow_html=True,
            )
            st.caption("Ringkasan sesuai filter saat ini.")
            st.download_button(
                "Unduh ringkasan CSV",
                data=_csv_ringkasan(daftar),
                file_name="riwayat-cekdbd.csv",
                mime="text/csv",
            )

    _tampilkan_ringkasan(daftar)
    st.caption(f"Menampilkan {len(daftar)} dari {len(semua)} pemeriksaan.")

    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    tema.bagian(
        "01",
        "Daftar Pemeriksaan",
        "Buka rincian untuk melihat perbandingan dan angka perhitungannya.",
    )

    if len(daftar) == 0:
        tema.kosong(
            "Tidak ada yang cocok",
            "Coba kata kunci lain, misalnya nama pasien, ID, atau solusi akhir.",
            "Kosongkan kolom pencarian untuk menampilkan seluruh pemeriksaan.",
        )
        return

    for k in daftar:
        detail = svc_riwayat.detail_konsultasi(k["id"])
        if len(detail) > 0:
            persentase = detail[0]["persentase"]
            nama_acuan = f"ID {detail[0]['kasus_id']} — {detail[0]['nama_kasus']}"
        else:
            persentase = (k["cosine_tertinggi"] or 0) * 100
            nama_acuan = f"ID {k['kasus_acuan_id']}"

        tema.kartu_riwayat(
            k["id"],
            k["nama_kasus_baru"],
            persentase,
            k["solusi_final"],
            k["dibuat_pada"],
        )
        with st.expander(f"Rincian #{k['id']} — {k['nama_kasus_baru']}"):
            tema.gauge(
                persentase,
                nama_acuan,
                f"Dicatat {k['dibuat_pada']}",
            )
            st.markdown('<hr class="hairline">', unsafe_allow_html=True)
            st.markdown(
                '<div class="card-kicker">Solusi akhir</div>',
                unsafe_allow_html=True,
            )
            tema.judul_kartu(k["solusi_final"])
            st.markdown(
                tema.meta_rows([
                    ("Rekomendasi awal", k["solusi_rekomendasi"]),
                    ("Sumber solusi", k["sumber_solusi"]),
                    ("Vektor input", format_vektor(k["vektor_baru"])),
                ]),
                unsafe_allow_html=True,
            )
            if k["catatan"]:
                st.write(f"**Catatan:** {k['catatan']}")

            if len(detail) > 0:
                st.markdown('<hr class="hairline">', unsafe_allow_html=True)
                st.write("**Perbandingan kasus:**")
                st.dataframe(
                    [
                        {
                            "Peringkat": d["peringkat"],
                            "ID Kasus": d["kasus_id"],
                            "Nama Kasus": d["nama_kasus"],
                            "Dot Product": round(d["dot_product"], 4),
                            "Panjang Baru": round(d["panjang_baru"], 4),
                            "Panjang Lama": round(d["panjang_lama"], 4),
                            "Cosine Similarity": round(d["cosine"], 4),
                            "Kemiripan (%)": round(d["persentase"], 2),
                        }
                        for d in detail
                    ],
                    width="stretch",
                    hide_index=True,
                )

                terbaik = detail[0]
                st.code(
                    "Cosine (peringkat 1) = "
                    f"{terbaik['dot_product']} / "
                    f"({round(terbaik['panjang_baru'], 4)} × "
                    f"{round(terbaik['panjang_lama'], 4)}) = "
                    f"{round(terbaik['cosine'], 4)}",
                    language="text",
                )
