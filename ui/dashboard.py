"""
Halaman Dashboard: ringkasan data, hasil terbaru, dan gambaran alur CBR.
"""

import streamlit as st

from services import kasus, kriteria, riwayat
from ui import tema
from ui.helper import format_vektor, tampilkan_flash


def _tampilkan_ringkasan():
    """Empat angka ringkasan yang diambil langsung dari database."""
    kol1, kol2, kol3, kol4 = st.columns(4)
    kol1.metric("Jumlah Kasus Tersimpan", kasus.total_kasus())
    kol2.metric("Jumlah Kriteria / Gejala", kriteria.total_kriteria())
    kol3.metric("Jumlah Konsultasi", riwayat.total_konsultasi())
    kol4.metric("Jumlah Perbandingan", riwayat.total_perbandingan())


def _tampilkan_riwayat_singkat():
    """Daftar 5 konsultasi terakhir sebagai gambaran aktivitas sistem."""
    daftar = riwayat.daftar_konsultasi()
    if len(daftar) == 0:
        return

    baris = []
    for k in daftar[:5]:
        cosine = k["cosine_tertinggi"]
        baris.append({
            "ID": k["id"],
            "Kasus Baru": k["nama_kasus_baru"],
            "Cosine Tertinggi": round(cosine, 4) if cosine is not None else 0,
            "Solusi Final": k["solusi_final"],
            "Waktu": k["dibuat_pada"],
        })

    tema.bagian(
        "🕘",
        "Riwayat Konsultasi Terakhir",
        "Lima konsultasi terbaru sebagai gambaran aktivitas sistem.",
        badge="Aktivitas",
        badge_tone="abu",
    )
    st.dataframe(baris, width="stretch", hide_index=True)


def _tampilkan_hasil_terbaru(terakhir, detail):
    """Kartu utama dashboard: gauge kemiripan + ringkasan tekstual."""
    tema.bagian(
        "🏆",
        "Hasil Perhitungan Terbaru",
        badge="Terbaru",
        badge_tone="hijau",
    )

    if len(detail) > 0:
        terbaik = detail[0]
        persentase = terbaik["persentase"]
        nama_acuan = f"ID {terbaik['kasus_id']} — {terbaik['nama_kasus']}"
        keterangan = f"Peringkat 1 · Cosine {round(terbaik['cosine'], 4)}"
    else:
        cosine = terakhir["cosine_tertinggi"]
        persentase = (cosine or 0) * 100
        nama_acuan = f"ID {terakhir['kasus_acuan_id']}"
        keterangan = "Kasus pembanding tidak tersedia"

    with st.container(border=True):
        tema.gauge(persentase, nama_acuan, keterangan)
        st.divider()
        st.write(f"**Kasus baru:** {terakhir['nama_kasus_baru']}")
        st.write(f"**Vektor input:** `{format_vektor(terakhir['vektor_baru'])}`")
        st.write(f"**Solusi final:** {terakhir['solusi_final']}")
        st.write(f"**Sumber solusi:** {terakhir['sumber_solusi']}")
        st.caption(f"Diproses pada {terakhir['dibuat_pada']}")


def _tampilkan_grafik(terakhir, detail):
    """Grafik batang persentase kemiripan konsultasi terakhir."""
    tema.bagian(
        "📈",
        "Perbandingan Kasus (Konsultasi Terakhir)",
        badge="Cosine Manual",
        badge_tone="biru",
    )
    if len(detail) == 0:
        st.info("Detail perbandingan untuk konsultasi ini tidak tersedia.")
        return

    grafik = {}
    for d in detail:
        grafik[f"ID {d['kasus_id']} - {d['nama_kasus']}"] = round(
            d["persentase"], 2
        )
    st.bar_chart(grafik, height=260)
    st.caption(
        "Semua nilai adalah persentase kemiripan hasil Cosine Similarity "
        "yang dihitung manual."
    )


def tampilkan():
    tema.header(
        "📊",
        "Dashboard",
        "Pantau basis pengetahuan, proses perhitungan, dan hasil terkini sistem.",
        badge="Ringkasan Sistem",
    )
    tampilkan_flash()

    _tampilkan_ringkasan()
    st.divider()

    terakhir = riwayat.konsultasi_terakhir()
    if terakhir is None:
        with st.container(border=True):
            tema.bagian(
                "🏆",
                "Hasil Perhitungan Terbaru",
                badge="Terbaru",
                badge_tone="hijau",
            )
            st.info(
                "Belum ada konsultasi. Buka menu **Konsultasi Baru** untuk "
                "memulai proses CBR."
            )
        st.divider()
        tema.bagian(
            "🧭",
            "Alur Metode CBR",
            "Empat tahap yang dilalui setiap kali sistem mencari solusi.",
            badge="CBR",
            badge_tone="biru",
        )
        tema.flow_cards()
        return

    detail = riwayat.detail_konsultasi(terakhir["id"])

    kol_kiri, kol_kanan = st.columns([1.05, 1], gap="large")
    with kol_kiri:
        _tampilkan_hasil_terbaru(terakhir, detail)
    with kol_kanan:
        _tampilkan_grafik(terakhir, detail)

    st.divider()
    tema.bagian(
        "🧭",
        "Alur Metode CBR",
        "Empat tahap yang dilalui setiap kali sistem mencari solusi.",
        badge="CBR",
        badge_tone="biru",
    )
    tema.flow_cards()

    st.divider()
    _tampilkan_riwayat_singkat()
