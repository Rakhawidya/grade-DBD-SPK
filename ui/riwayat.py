"""
Halaman Riwayat Perhitungan.

Menampilkan seluruh konsultasi beserta detail perbandingan yang pernah
dilakukan, sehingga proses perhitungan lama tetap dapat diaudit.
"""

import streamlit as st

from services import riwayat as svc_riwayat
from ui import tema
from ui.helper import format_vektor, tampilkan_flash


def tampilkan():
    tema.header(
        "📜",
        "Riwayat Perhitungan",
        "Seluruh konsultasi yang pernah diproses, lengkap dengan detail "
        "Cosine Similarity tiap kasus pembanding.",
        badge="Audit Perhitungan",
        badge_tone="kuning",
    )
    tampilkan_flash()

    daftar = svc_riwayat.daftar_konsultasi()
    kartu1, kartu2, kartu3 = st.columns(3)
    with kartu1:
        tema.kartu_ringkas(
            "Total Konsultasi", svc_riwayat.total_konsultasi(), "proses CBR tercatat"
        )
    with kartu2:
        tema.kartu_ringkas(
            "Total Perbandingan",
            svc_riwayat.total_perbandingan(),
            "baris perhitungan kasus",
        )
    with kartu3:
        tema.kartu_ringkas(
            "Riwayat Ditampilkan", len(daftar), "konsultasi terbaru di atas"
        )
    st.divider()

    tema.bagian(
        "📂",
        "Daftar Konsultasi",
        "Buka salah satu konsultasi untuk melihat angka perhitungan lengkap.",
        badge="Audit",
        badge_tone="abu",
    )

    if len(daftar) == 0:
        st.info("Belum ada riwayat konsultasi.")
        return

    for k in daftar:
        detail = svc_riwayat.detail_konsultasi(k["id"])
        if len(detail) > 0:
            persentase = detail[0]["persentase"]
            nama_acuan = f"ID {detail[0]['kasus_id']} — {detail[0]['nama_kasus']}"
        else:
            persentase = (k["cosine_tertinggi"] or 0) * 100
            nama_acuan = f"ID {k['kasus_acuan_id']}"

        judul = (
            f"#{k['id']} — {k['nama_kasus_baru']} | "
            f"kemiripan {round(persentase, 1)}% | "
            f"{k['dibuat_pada']}"
        )
        with st.expander(judul):
            # --- Ringkasan konsultasi -----------------------------------
            tema.gauge(
                persentase,
                nama_acuan,
                f"Solusi final: {k['solusi_final']}",
            )
            st.divider()
            st.write(f"**Vektor input:** `{format_vektor(k['vektor_baru'])}`")
            st.write(f"**Solusi rekomendasi (Reuse):** {k['solusi_rekomendasi']}")
            st.write(f"**Solusi final (setelah Revise):** {k['solusi_final']}")
            st.write(f"**Sumber solusi:** {k['sumber_solusi']}")
            if k["catatan"]:
                st.write(f"**Catatan peninjauan:** {k['catatan']}")
            st.caption(f"Kasus acuan: ID {k['kasus_acuan_id']}")

            # --- Detail perbandingan ------------------------------------
            if detail:
                st.write("**Detail perbandingan kasus:**")
                st.dataframe(
                    [
                        {
                            "Peringkat": d["peringkat"],
                            "ID Kasus": d["kasus_id"],
                            "Nama Kasus": d["nama_kasus"],
                            "Dot Product": round(d["dot_product"], 4),
                            "Panjang Vektor Baru": round(d["panjang_baru"], 4),
                            "Panjang Vektor Lama": round(d["panjang_lama"], 4),
                            "Cosine Similarity": round(d["cosine"], 4),
                            "Kemiripan (%)": round(d["persentase"], 2),
                        }
                        for d in detail
                    ],
                    width="stretch",
                    hide_index=True,
                )

                # Rumus untuk kasus peringkat 1, agar mudah dijelaskan.
                terbaik = detail[0]
                st.code(
                    "Cosine (peringkat 1) = "
                    f"{terbaik['dot_product']} / "
                    f"({round(terbaik['panjang_baru'], 4)} x "
                    f"{round(terbaik['panjang_lama'], 4)}) = "
                    f"{round(terbaik['cosine'], 4)}",
                    language="text",
                )
