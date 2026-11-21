"""
Tampilan bersama (tema modern) untuk seluruh halaman Streamlit.

File ini hanya berisi CSS dan pembantu penyusun komponen visual. Ia tidak
menyentuh logika CBR maupun database. Semua warna, sudut kartu, bayangan,
dan komponen didefinisikan di sini supaya tampilan konsisten dan mudah
diubah di satu tempat.
"""

from html import escape

import streamlit as st

_CSS = """
<style>
/* ===================== Palet & dasar ===================== */
:root {
    --spk-primary: #0f766e;
    --spk-primary-2: #0ea5e9;
    --spk-ink: #0f172a;
    --spk-muted: #64748b;
    --spk-line: #e2e8f0;
    --spk-soft: #f8fafc;
    --spk-mint: #ecfdf5;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 0% 0%, #ecfeff 0%, rgba(236,254,255,0) 34%),
        radial-gradient(circle at 100% 0%, #eef2ff 0%, rgba(238,242,255,0) 30%),
        var(--spk-soft);
}

h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    background: linear-gradient(120deg, var(--spk-primary), var(--spk-primary-2));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}

/* ===================== Sidebar ===================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f766e 0%, #115e59 45%, #0b3b46 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #e6fffb !important; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 10px;
    font-weight: 600;
    padding: 0.45rem 0.6rem;
    transition: background 0.15s ease, transform 0.15s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.12);
    transform: translateX(2px);
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.18) !important; }

.spk-side-logo {
    align-items: center;
    display: flex;
    gap: 0.7rem;
    margin-bottom: 0.35rem;
}
.spk-side-logo .ikon {
    align-items: center;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 14px;
    display: inline-flex;
    font-size: 1.5rem;
    height: 2.9rem;
    justify-content: center;
    width: 2.9rem;
}
.spk-side-logo .judul { font-size: 1.05rem; font-weight: 800; line-height: 1.15; }
.spk-side-logo .sub { font-size: 0.72rem; opacity: 0.78; }

.spk-side-card {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 14px;
    color: #d1fae5 !important;
    font-size: 0.82rem;
    line-height: 1.55;
    padding: 0.8rem 0.9rem;
}
.spk-side-card b { color: #ffffff !important; }
.spk-side-status {
    background: rgba(16,185,129,0.22);
    border: 1px solid rgba(110,231,183,0.35);
    border-radius: 999px;
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 0.6rem;
    padding: 0.22rem 0.65rem;
}

/* ===================== Header & badge ===================== */
.spk-hero {
    background: linear-gradient(135deg, #0f766e 0%, #0e7490 55%, #1e3a8a 100%);
    border-radius: 20px;
    box-shadow: 0 12px 28px rgba(15,118,110,0.22);
    color: #ffffff !important;
    margin: 0.35rem 0 1rem 0;
    overflow: hidden;
    padding: 1.15rem 1.35rem;
    position: relative;
}
.spk-hero::after {
    border: 22px solid rgba(255,255,255,0.08);
    border-radius: 50%;
    content: "";
    height: 150px;
    position: absolute;
    right: -42px;
    top: -62px;
    width: 150px;
}
.spk-hero .isi { position: relative; z-index: 1; }
.spk-hero p { color: #d1fae5 !important; margin: 0.3rem 0 0; }

.spk-badge {
    background: #ccfbf1;
    border-radius: 999px;
    color: #0f766e;
    display: inline-block;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    margin: 0 0.45rem 0.35rem 0;
    padding: 0.25rem 0.7rem;
    text-transform: uppercase;
}
.spk-badge.biru { background: #e0f2fe; color: #0369a1; }
.spk-badge.hijau { background: #d1fae5; color: #065f46; }
.spk-badge.kuning { background: #fef3c7; color: #92400e; }
.spk-badge.abu { background: #e2e8f0; color: #475569; }

/* ===================== Penanda tahap CBR ===================== */
.spk-stepper { display: flex; flex-wrap: wrap; gap: 0.55rem; margin: 0 0 1.15rem 0; }
.spk-step {
    align-items: center;
    background: #ffffff;
    border: 1px solid var(--spk-line);
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04);
    color: var(--spk-muted);
    display: flex;
    flex: 1 1 130px;
    font-size: 0.84rem;
    font-weight: 700;
    gap: 0.5rem;
    padding: 0.7rem 0.8rem;
}
.spk-step .nomor {
    align-items: center;
    background: #f1f5f9;
    border-radius: 50%;
    display: inline-flex;
    flex: 0 0 1.65rem;
    font-size: 0.78rem;
    height: 1.65rem;
    justify-content: center;
}
.spk-step.selesai { background: var(--spk-mint); border-color: #a7f3d0; color: #065f46; }
.spk-step.selesai .nomor { background: #a7f3d0; }
.spk-step.aktif {
    background: linear-gradient(135deg, var(--spk-primary), var(--spk-primary-2));
    border-color: transparent;
    box-shadow: 0 8px 18px rgba(14,165,233,0.25);
    color: #ffffff;
    transform: translateY(-2px);
}
.spk-step.aktif .nomor { background: rgba(255,255,255,0.22); color: #ffffff; }

/* ===================== Kartu metrik & konten ===================== */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border: 1px solid var(--spk-line);
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(15,23,42,0.06);
    overflow: hidden;
    padding: 0.9rem 1rem;
    position: relative;
}
div[data-testid="stMetric"]::before {
    background: linear-gradient(180deg, #14b8a6, var(--spk-primary));
    content: "";
    height: 100%;
    left: 0;
    position: absolute;
    top: 0;
    width: 4px;
}
div[data-testid="stMetricLabel"] p {
    color: var(--spk-muted) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricValue"] {
    color: var(--spk-primary) !important;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--spk-line) !important;
    border-radius: 16px !important;
    box-shadow: 0 6px 18px rgba(15,23,42,0.05);
}
[data-testid="stForm"] {
    background: rgba(255,255,255,0.78);
    border: 1px solid #cbd5e1 !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}
[data-testid="stExpander"] {
    border: 1px solid var(--spk-line) !important;
    border-radius: 14px !important;
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--spk-line);
    border-radius: 14px;
    overflow: hidden;
}

/* Kerapian kecil yang sering terlihat: judul bagian, notifikasi, kode. */
h2 {
    color: var(--spk-ink) !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em;
    margin-top: 0.35rem !important;
}
[data-testid="stExpander"] summary {
    color: var(--spk-ink) !important;
    font-weight: 700 !important;
}
[data-testid="stAlert"] { border-radius: 12px !important; }
pre {
    border-radius: 12px !important;
    font-size: 0.82rem !important;
}
[data-testid="stCheckbox"] label { cursor: pointer; }

button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, var(--spk-primary), var(--spk-primary-2)) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 14px rgba(15,118,110,0.22);
}
button[data-testid="baseButton-secondary"] { border-radius: 10px !important; }

/* ===================== Kartu HTML tambahan ===================== */
.spk-card {
    background: #ffffff;
    border: 1px solid var(--spk-line);
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.06);
    padding: 1rem 1.1rem;
}
.spk-card .judul { color: var(--spk-ink); font-size: 0.82rem; font-weight: 800; letter-spacing: 0.04em; text-transform: uppercase; }
.spk-card .nilai { color: var(--spk-primary); font-size: 1.45rem; font-weight: 800; margin-top: 0.25rem; }
.spk-card .petunjuk { color: var(--spk-muted); font-size: 0.8rem; margin-top: 0.2rem; }

.spk-gauge-wrap { align-items: center; display: flex; gap: 1rem; }
.spk-gauge {
    align-items: center;
    border-radius: 50%;
    display: flex;
    flex: 0 0 112px;
    height: 112px;
    justify-content: center;
    position: relative;
    width: 112px;
}
.spk-gauge::before {
    background: #ffffff;
    border-radius: 50%;
    content: "";
    height: 86px;
    position: absolute;
    width: 86px;
}
.spk-gauge .teks { position: relative; text-align: center; z-index: 1; }
.spk-gauge .teks b { color: var(--spk-ink); font-size: 1.35rem; line-height: 1; }
.spk-gauge .teks small { color: var(--spk-muted); font-size: 0.7rem; }
.spk-gauge-info .nama { color: var(--spk-ink); font-size: 1.05rem; font-weight: 800; }
.spk-gauge-info .baris { color: var(--spk-muted); font-size: 0.85rem; margin-top: 0.35rem; }

.spk-flow { display: grid; gap: 0.6rem; grid-template-columns: repeat(4, minmax(0, 1fr)); }
.spk-flow-item {
    background: #ffffff;
    border: 1px solid var(--spk-line);
    border-radius: 14px;
    padding: 0.8rem;
}
.spk-flow-item .ikon { font-size: 1.2rem; }
.spk-flow-item .nama { color: var(--spk-ink); font-size: 0.85rem; font-weight: 800; margin-top: 0.25rem; }
.spk-flow-item .ket { color: var(--spk-muted); font-size: 0.74rem; margin-top: 0.2rem; }

@media (max-width: 900px) {
    .spk-flow { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 640px) {
    h1 { font-size: 1.55rem !important; }
    .spk-step { flex: 1 1 100%; }
    .spk-gauge-wrap { flex-direction: column; align-items: flex-start; }
    .spk-flow { grid-template-columns: 1fr; }
}
</style>
"""

_TAHAPAN = [
    ("Retrieve", "🔎", "Cari kasus paling mirip"),
    ("Reuse", "♻️", "Ambil solusi awal"),
    ("Revise", "✍️", "Tinjau & validasi"),
    ("Retain", "💾", "Simpan kasus baru"),
]

_IKON_MENU = {
    "Dashboard": "📊",
    "Konsultasi Baru": "🩺",
    "Manajemen Kasus": "🗂️",
    "Manajemen Kriteria": "⚙️",
    "Riwayat Perhitungan": "📜",
}


def terapkan_tema():
    """Menyuntikkan CSS sekali setiap kali aplikasi dijalankan ulang."""
    st.markdown(_CSS, unsafe_allow_html=True)


def ikon_menu(nama):
    """Label menu sidebar dengan ikon (nilai radio asli tetap dipakai UI)."""
    return f"{_IKON_MENU.get(nama, '•')} {nama}"


def sidebar_hero():
    """Kartu identitas aplikasi di bagian atas sidebar."""
    return """
    <div class="spk-side-logo">
        <span class="ikon">🩺</span>
        <div>
            <div class="judul">SPK CBR — DBD</div>
            <div class="sub">Sistem Pendukung Keputusan</div>
        </div>
    </div>
    """


def sidebar_info():
    """Ringkasan metode dan status database di sidebar."""
    return """
    <div class="spk-side-card">
        <b>Alur CBR</b><br>
        Retrieve → Reuse → Revise → Retain<br><br>
        <b>Kemiripan</b><br>
        Cosine Similarity dihitung manual dengan Python dasar.
        <div class="spk-side-status">● Database aktif</div>
    </div>
    """


def header(ikon, judul, deskripsi, badge=None, badge_tone=""):
    """
    Judul tetap memakai st.title (mudah diuji), ditambah hero card dan badge.
    """
    st.title(f"{ikon} {judul}")
    kelas = f"spk-badge {badge_tone}".strip()
    lencana = f'<span class="{kelas}">{escape(str(badge))}</span>' if badge else ""
    st.markdown(
        '<div class="spk-hero"><div class="isi">'
        f"{lencana}<p>{escape(str(deskripsi))}</p>"
        "</div></div>",
        unsafe_allow_html=True,
    )


def langkah_cbr(aktif):
    """
    Menampilkan empat tahap CBR. Tahap sebelum `aktif` ditandai selesai.
    """
    indeks_aktif = -1
    for i, (nama, _ikon, _ket) in enumerate(_TAHAPAN):
        if nama == aktif:
            indeks_aktif = i

    bagian = []
    for i, (nama, ikon, _ket) in enumerate(_TAHAPAN):
        if i == indeks_aktif:
            kelas = "aktif"
        elif indeks_aktif > i:
            kelas = "selesai"
        else:
            kelas = ""
        bagian.append(
            f'<div class="spk-step {kelas}">'
            f'<span class="nomor">{i + 1}</span>{ikon} {nama}</div>'
        )

    st.markdown(
        '<div class="spk-stepper">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def bagian(ikon, judul, keterangan="", badge=None, badge_tone=""):
    """Judul bagian yang konsisten: badge → subheader → caption."""
    if badge:
        kelas = f"spk-badge {badge_tone}".strip()
        st.markdown(
            f'<span class="{kelas}">{escape(str(badge))}</span>',
            unsafe_allow_html=True,
        )
    st.subheader(f"{ikon} {judul}")
    if keterangan:
        st.caption(keterangan)


def flow_cards():
    """Empat kartu penjelas tahap CBR untuk dashboard."""
    bagian = []
    for i, (nama, ikon, ket) in enumerate(_TAHAPAN):
        bagian.append(
            '<div class="spk-flow-item">'
            f'<div class="ikon">{ikon}</div>'
            f'<div class="nama">{i + 1}. {nama}</div>'
            f'<div class="ket">{ket}</div>'
            "</div>"
        )
    st.markdown(
        '<div class="spk-flow">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def kartu_ringkas(judul, nilai, petunjuk):
    """Kartu kecil untuk angka-angka ringkasan tambahan."""
    st.markdown(
        '<div class="spk-card">'
        f'<div class="judul">{escape(str(judul))}</div>'
        f'<div class="nilai">{escape(str(nilai))}</div>'
        f'<div class="petunjuk">{escape(str(petunjuk))}</div>'
        "</div>",
        unsafe_allow_html=True,
    )


def gauge(persentase, nama_kasus, keterangan=""):
    """
    Indikator kemiripan berbentuk cincin.

    `persentase` sudah dihitung di core/cbr.py; di sini hanya dibatasi agar
    tetap berada di rentang 0–100 untuk keperluan tampilan.
    """
    nilai = float(persentase)
    if nilai < 0:
        nilai = 0.0
    if nilai > 100:
        nilai = 100.0
    derajat = round(nilai * 3.6, 1)

    if nilai >= 75:
        warna = "#10b981"
    elif nilai >= 50:
        warna = "#0ea5e9"
    else:
        warna = "#f59e0b"

    gaya = (
        f"background:conic-gradient({warna} {derajat}deg, #e2e8f0 {derajat}deg 360deg);"
    )
    ket = f'<div class="baris">{escape(str(keterangan))}</div>' if keterangan else ""

    st.markdown(
        '<div class="spk-gauge-wrap">'
        f'<div class="spk-gauge" style="{gaya}">'
        f'<div class="teks"><b>{round(nilai, 1)}%</b><br><small>kemiripan</small></div>'
        "</div>"
        '<div class="spk-gauge-info">'
        f'<div class="nama">{escape(str(nama_kasus))}</div>'
        f"{ket}"
        "</div></div>",
        unsafe_allow_html=True,
    )
