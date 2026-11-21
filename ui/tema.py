"""
Gaya visual bersama untuk CEKDBD.

File ini hanya berisi CSS dan fungsi penyusun tampilan. Tidak ada perhitungan
CBR di sini. Semua warna, tipografi, ruang, radius, dan bayangan didefinisikan
sebagai token di `:root` supaya perubahan desain cukup dilakukan di satu tempat.

Catatan selector: sebagian aturan memakai atribut `data-testid` / `data-baseweb`
milik Streamlit. Itu selector internal yang bisa berubah antarversi, jadi setiap
penggunaannya diberi komentar dan dipusatkan di file ini.
"""

from html import escape

import streamlit as st

_CSS = """
<style>
:root {
    /* Mode terang dipaksa, termasuk saat perangkat memakai tema gelap. */
    color-scheme: light only;

    /* Warna */
    --bg: #f5f6f4;
    --surface: #ffffff;
    --surface-alt: #fbfcfa;
    --ink: #17231f;
    --muted: #5f6e68;
    --line: #e2e8e4;
    --line-soft: #edf1ee;
    --accent: #176b56;
    --accent-dark: #0f523f;
    --accent-soft: #e9f4ef;
    /* Satu warna peringatan saja. Gelap agar teks lulus WCAG AA di atas putih. */
    --warning: #8f5716;
    --warning-dark: #74430f;
    --warning-soft: #fbf1e3;
    --warning-line: #e8d2b4;
    --focus: rgba(23, 107, 86, 0.22);
    --focus-warning: rgba(143, 87, 22, 0.24);
    --hover: #f0f4f1;

    /* Ruang */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;

    /* Radius & bayangan */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-pill: 999px;
    --shadow-sm: 0 1px 2px rgba(23, 35, 31, 0.05);
    --shadow-md: 0 10px 28px rgba(23, 35, 31, 0.07);

    /* Tipografi */
    --font-ui: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    --font-display: Georgia, "Times New Roman", serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
    --text-xs: 0.72rem;
    --text-sm: 0.82rem;
    --text-md: 0.95rem;
    --text-lg: 1.1rem;
    --text-xl: 1.45rem;
    --text-2xl: 2.05rem;
}

/* ---------- Dasar ---------- */
html, body, [class*="css"] {
    font-family: var(--font-ui);
}
html, body {
    background: var(--bg);
    color: var(--ink);
}
/* Selector internal Streamlit: aplikasi root. */
[data-testid="stApp"] { color-scheme: light only; }
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: var(--bg);
}

/* Streamlit mewarisi warna sistem. Kunci ke palet terang agar teks tidak
   berubah saat perangkat berada di mode gelap. */
[data-testid="stMarkdownContainer"] p:not(.lead),
[data-testid="stMarkdownContainer"] li,
[data-testid="stWidgetLabel"] p,
[data-testid="stCheckbox"] label p {
    color: var(--ink) !important;
}
[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 2.1rem;
    padding-bottom: var(--space-6);
}

h1 {
    color: var(--ink) !important;
    font-size: var(--text-2xl) !important;
    font-weight: 700 !important;
    letter-spacing: -0.035em;
    margin: var(--space-2) 0 var(--space-3) !important;
}
h2 {
    color: var(--ink) !important;
    font-size: 1.08rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
    margin: var(--space-3) 0 var(--space-2) !important;
}
h3 {
    color: var(--ink) !important;
    font-size: var(--text-md) !important;
    font-weight: 700 !important;
}
p, li { line-height: 1.65; }

/* ---------- Sidebar ---------- */
/* Selector internal Streamlit: sidebar dan radio navigasi. */
[data-testid="stSidebar"] {
    background: var(--surface-alt);
    border-right: 1px solid var(--line);
    color-scheme: light only;
}
[data-testid="stSidebar"] * { color: var(--ink) !important; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.55rem 0.7rem;
    transition: background 0.15s ease, color 0.15s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: var(--hover);
}
/* Opsi aktif ditandai aria-checked oleh Streamlit. */
[data-testid="stSidebar"] [role="radio"][aria-checked="true"],
[data-testid="stSidebar"] label:has(input:checked) {
    background: var(--accent-soft) !important;
    box-shadow: inset 3px 0 0 var(--accent);
    color: var(--accent-dark) !important;
}
[data-testid="stSidebar"] hr { border-color: var(--line) !important; }

.brand {
    align-items: center;
    border-bottom: 1px solid var(--line);
    display: flex;
    gap: var(--space-3);
    margin-bottom: var(--space-5);
    padding: var(--space-1) var(--space-1) var(--space-4);
}
.brand-mark {
    align-items: center;
    background: var(--accent);
    border-radius: 10px;
    box-shadow: var(--shadow-sm);
    color: #ffffff !important;
    display: inline-flex;
    flex: 0 0 38px;
    font-family: var(--font-display);
    font-size: 1.55rem;
    height: 38px;
    justify-content: center;
    line-height: 1;
}
.brand-name {
    color: var(--ink) !important;
    font-family: var(--font-display);
    font-size: 1.32rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    line-height: 1.1;
}
.brand-tag {
    color: var(--muted) !important;
    font-size: var(--text-xs);
    line-height: 1.35;
    margin-top: var(--space-1);
}
.side-note {
    border-top: 1px solid var(--line);
    color: var(--muted) !important;
    font-size: var(--text-xs);
    line-height: 1.6;
    margin-top: var(--space-4);
    padding-top: var(--space-3);
}
.side-note b { color: var(--ink) !important; }

/* ---------- Header halaman ---------- */
.eyebrow {
    color: var(--accent) !important;
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.lead {
    color: var(--muted) !important;
    font-size: var(--text-md);
    margin: var(--space-1) 0 var(--space-5);
    max-width: 760px;
}
.section-number {
    color: var(--accent) !important;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 600;
    letter-spacing: 0.12em;
    margin-bottom: var(--space-1);
}
.card-kicker {
    color: var(--muted) !important;
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.14em;
    margin-bottom: var(--space-3);
    text-transform: uppercase;
}
.card-title {
    color: var(--ink);
    font-family: var(--font-display);
    font-size: 1.35rem;
    line-height: 1.3;
    margin: 0 0 var(--space-3);
    overflow-wrap: anywhere;
}
.card-title.lg {
    font-size: var(--text-xl);
    margin-bottom: var(--space-2);
}
.hairline {
    background: var(--line);
    border: 0;
    height: 1px;
    margin: var(--space-5) 0;
}

/* ---------- Permukaan, form, tabel ---------- */
/* Selector internal Streamlit: container bordered, form, expander, dataframe. */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
}
[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md);
    padding: var(--space-5) !important;
}
[data-testid="stExpander"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md);
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: var(--ink) !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    max-width: 100%;
    overflow-x: auto;
}
[data-testid="stAlert"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md) !important;
    font-size: var(--text-sm);
}
/* Selector internal Streamlit: kind dipakai baseweb pada notifikasi. */
[data-testid="stAlert"]:has([kind="success"]) {
    border-left: 3px solid var(--accent) !important;
}
[data-testid="stAlert"]:has([kind="warning"]),
[data-testid="stAlert"]:has([kind="danger"]),
[data-testid="stAlert"]:has([kind="error"]) {
    border-left: 3px solid var(--warning) !important;
}

div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    padding: 0.85rem var(--space-4);
    transition: border-color 0.15s ease, transform 0.15s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
}
div[data-testid="stMetric"]::before { display: none; }
div[data-testid="stMetricLabel"] p {
    color: var(--muted) !important;
    font-size: var(--text-sm) !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    font-variant-numeric: tabular-nums;
}

/* ---------- Tombol ---------- */
/* Selector internal Streamlit: baseButton. */
button[data-testid="baseButton-primary"] {
    background: var(--accent) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: var(--shadow-sm) !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.05rem !important;
    transition: background 0.15s ease, transform 0.08s ease;
}
button[data-testid="baseButton-primary"]:hover { background: var(--accent-dark) !important; }
button[data-testid="baseButton-primary"]:active { transform: translateY(1px); }
button[data-testid="baseButton-secondary"] {
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color 0.15s ease, color 0.15s ease;
}
button[data-testid="baseButton-secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent-dark) !important;
}
button[data-testid="baseButton-primary"]:focus-visible,
button[data-testid="baseButton-secondary"]:focus-visible {
    box-shadow: 0 0 0 3px var(--focus) !important;
    outline: none;
}
/* CTA di hero sedikit lebih besar dari tombol biasa. */
.hero-actions [data-testid="stButton"] button {
    padding: 0.7rem 1.3rem !important;
}

/* ---------- Input & fokus ---------- */
/* Selector internal Streamlit: baseweb dipakai input/textarea/checkbox. */
[data-testid="stCheckbox"] label { cursor: pointer; }
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    border-radius: var(--radius-sm) !important;
    font-size: var(--text-md);
}
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--focus) !important;
}
[data-baseweb="checkbox"] input:checked + div {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ---------- Indikator langkah ---------- */
.steps {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    display: flex;
    margin-bottom: var(--space-5);
    overflow: hidden;
}
.step {
    border-right: 1px solid var(--line);
    flex: 1;
    padding: 0.75rem 0.95rem;
    position: relative;
}
.step:last-child { border-right: 0; }
.step-no {
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 600;
    letter-spacing: 0.1em;
}
.step-name {
    display: block;
    font-size: 0.88rem;
    font-weight: 700;
    margin-top: var(--space-1);
}
.step-note {
    color: var(--muted);
    display: block;
    font-size: var(--text-xs);
    margin-top: 2px;
}
.step.done .step-no { color: var(--accent); }
.step.done .step-no::after { content: "  ✓"; }
.step.active { background: var(--accent-soft); }
.step.active::after {
    background: var(--accent);
    bottom: 0;
    content: "";
    height: 3px;
    left: 0;
    position: absolute;
    right: 0;
}

/* ---------- Ringkasan & status ---------- */
.summary-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 0.85rem var(--space-4);
}
.summary-card .label {
    color: var(--muted);
    font-size: var(--text-sm);
    font-weight: 600;
}
.summary-card .value {
    color: var(--ink);
    font-size: var(--text-xl);
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    line-height: 1.25;
    margin-top: var(--space-1);
}
.summary-card .hint {
    color: var(--muted);
    font-size: var(--text-xs);
    margin-top: var(--space-1);
}

.status-badge {
    align-items: center;
    border: 1px solid transparent;
    border-radius: var(--radius-pill);
    display: inline-flex;
    font-size: var(--text-xs);
    font-weight: 700;
    gap: var(--space-1);
    padding: 0.2rem 0.55rem;
}
.status-badge::before {
    background: currentColor;
    border-radius: 50%;
    content: "";
    height: 6px;
    width: 6px;
}
.status-badge--aman {
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent-dark);
}
.status-badge--perhatian {
    background: var(--warning-soft);
    border-color: var(--warning-line);
    color: var(--warning-dark);
}
.status-dot {
    border-radius: 50%;
    display: inline-block;
    height: 7px;
    margin-left: var(--space-2);
    width: 7px;
}
.status-dot--aman { background: var(--accent); }
.status-dot--perhatian { background: var(--warning); }

/* ---------- Gauge ---------- */
.gauge-wrap { align-items: center; display: flex; gap: var(--space-5); }
.gauge {
    /* Hanya sudut dinamis yang memakai inline style. Warna ada di class. */
    align-items: center;
    background: conic-gradient(var(--gauge-color) var(--derajat), var(--line) var(--derajat) 360deg);
    border-radius: 50%;
    display: flex;
    flex: 0 0 112px;
    height: 112px;
    justify-content: center;
    position: relative;
    width: 112px;
}
.gauge--aman { --gauge-color: var(--accent); }
.gauge--perhatian { --gauge-color: var(--warning); }
.gauge::before {
    background: var(--surface);
    border-radius: 50%;
    content: "";
    height: 88px;
    position: absolute;
    width: 88px;
}
.gauge .teks { position: relative; text-align: center; z-index: 1; }
.gauge .teks b {
    color: var(--ink);
    font-size: 1.45rem;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
    line-height: 1;
}
.gauge .teks small { color: var(--muted); font-size: var(--text-xs); }
.gauge-info .label {
    color: var(--muted);
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.gauge-info .nama {
    color: var(--ink);
    font-family: var(--font-display);
    font-size: 1.3rem;
    margin: var(--space-1) 0 var(--space-2);
}
.gauge-badges { margin: var(--space-2) 0 var(--space-1); }
.gauge-info .baris {
    color: var(--muted);
    font-size: var(--text-sm);
    margin-top: var(--space-1);
}

/* ---------- Komponen editorial ---------- */
.hero-title {
    color: var(--ink);
    font-family: var(--font-display);
    font-size: var(--text-2xl);
    letter-spacing: -0.02em;
    line-height: 1.14;
    margin: var(--space-1) 0 var(--space-3);
}
.hero-copy {
    color: var(--muted) !important;
    font-size: var(--text-md);
    max-width: 58ch;
}
.hero-actions {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-3) var(--space-5);
    margin-top: var(--space-5);
}
.hero-actions small { color: var(--muted); font-size: var(--text-sm); }
.hero-aside {
    /* Gradasi sangat tipis hanya untuk memisahkan panel ringkasan dari hero. */
    background: linear-gradient(180deg, var(--surface) 0%, var(--surface-alt) 100%);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    height: 100%;
    padding: var(--space-5);
}
.meta-list { margin: var(--space-1) 0 0; }
.meta-row {
    align-items: baseline;
    border-bottom: 1px solid var(--line-soft);
    display: flex;
    font-size: var(--text-sm);
    gap: var(--space-4);
    justify-content: space-between;
    padding: var(--space-3) 0;
}
.meta-row:last-child { border-bottom: 0; }
.meta-row span { color: var(--muted); }
.meta-row b { font-variant-numeric: tabular-nums; font-weight: 700; }

.pill-row { display: flex; flex-wrap: wrap; gap: var(--space-2); margin: var(--space-2) 0 0; }
.pill {
    background: var(--surface-alt);
    border: 1px solid var(--line);
    border-radius: 6px;
    color: var(--ink);
    font-size: var(--text-sm);
    padding: 0.25rem 0.55rem;
}
.pill::before {
    background: var(--accent);
    border-radius: 50%;
    content: "";
    display: inline-block;
    height: 5px;
    margin-right: var(--space-2);
    vertical-align: middle;
    width: 5px;
}

.note {
    background: var(--surface-alt);
    border-left: 3px solid var(--accent);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    color: var(--muted) !important;
    font-size: var(--text-sm);
    margin: var(--space-1) 0 var(--space-4);
    padding: var(--space-3);
}
.note--warning {
    background: var(--warning-soft);
    border-left-color: var(--warning);
    color: var(--warning-dark) !important;
}

.empty-state {
    background: var(--surface-alt);
    border: 1px dashed var(--line);
    border-radius: var(--radius-lg);
    padding: var(--space-5);
}
.empty-state .empty-title {
    color: var(--ink);
    font-family: var(--font-display);
    font-size: 1.2rem;
    margin-bottom: var(--space-2);
}
.empty-state .empty-copy {
    color: var(--muted) !important;
    font-size: var(--text-sm);
    margin: 0;
}

/* ---------- Daftar ringkas ---------- */
.peringkat-list, .aktivitas-list { display: grid; gap: var(--space-2); }
.peringkat-baris {
    align-items: center;
    display: grid;
    font-size: var(--text-sm);
    gap: var(--space-3);
    grid-template-columns: 26px minmax(0, 1fr) 110px 72px;
}
.peringkat-no { color: var(--muted); font-family: var(--font-mono); font-size: var(--text-xs); }
.peringkat-nama { min-width: 0; overflow-wrap: anywhere; }
.peringkat-bar { background: var(--line); border-radius: var(--radius-pill); height: 5px; overflow: hidden; }
.peringkat-bar i { background: var(--accent); display: block; height: 100%; }
.peringkat-bar i.perhatian { background: var(--warning); }
.peringkat-nilai { font-variant-numeric: tabular-nums; font-weight: 700; text-align: right; }

.aktivitas-baris {
    align-items: baseline;
    border-bottom: 1px solid var(--line-soft);
    display: grid;
    gap: var(--space-3);
    grid-template-columns: 42px minmax(0, 1fr) auto;
    padding: var(--space-3) 0;
}
.aktivitas-baris:last-child { border-bottom: 0; }
.aktivitas-id { color: var(--muted); font-family: var(--font-mono); font-size: var(--text-xs); }
.aktivitas-isi b { display: block; font-size: 0.88rem; }
.aktivitas-isi small { color: var(--muted); display: block; font-size: var(--text-xs); }
.aktivitas-waktu { color: var(--muted); font-size: var(--text-xs); white-space: nowrap; }

.quick-list { display: grid; gap: var(--space-3); grid-template-columns: repeat(3, minmax(0, 1fr)); }
.quick-item { border-top: 2px solid var(--line); padding-top: var(--space-3); }
.quick-item span { color: var(--accent); font-family: var(--font-mono); font-size: var(--text-xs); }
.quick-item b { display: block; font-size: 0.88rem; margin-top: var(--space-1); }
.quick-item small { color: var(--muted); font-size: var(--text-xs); }

/* ---------- Kelompok gejala & kartu riwayat ---------- */
.gejala-grup-judul {
    border-top: 1px solid var(--line-soft);
    color: var(--accent-dark) !important;
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.12em;
    margin: var(--space-4) 0 var(--space-2);
    padding-top: var(--space-3);
    text-transform: uppercase;
}
.gejala-grup-judul:first-of-type {
    border-top: 0;
    margin-top: 0;
    padding-top: 0;
}

.riwayat-kartu {
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    margin-bottom: var(--space-3);
    padding: var(--space-4);
}
.riwayat-kartu--perhatian { border-left-color: var(--warning); }
.riwayat-top {
    align-items: flex-start;
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2) var(--space-4);
    justify-content: space-between;
}
.riwayat-identitas { min-width: 0; }
.riwayat-id {
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 600;
}
.riwayat-judul {
    color: var(--ink);
    font-family: var(--font-display);
    font-size: 1.15rem;
    line-height: 1.3;
    margin-top: var(--space-1);
    overflow-wrap: anywhere;
}
.riwayat-nilai {
    color: var(--ink);
    font-size: 1.55rem;
    font-variant-numeric: tabular-nums;
    font-weight: 700;
    line-height: 1;
}
.riwayat-nilai small { color: var(--muted); font-size: var(--text-xs); font-weight: 500; }
.riwayat-meta {
    color: var(--muted);
    display: flex;
    flex-wrap: wrap;
    font-size: var(--text-sm);
    gap: var(--space-2) var(--space-4);
    margin-top: var(--space-2);
}
.riwayat-meta span { overflow-wrap: anywhere; }
.riwayat-meta b { color: var(--ink); font-weight: 600; }
.riwayat-badges { align-items: center; display: flex; gap: var(--space-2); }

.flow-list {
    display: grid;
    gap: var(--space-3);
    grid-template-columns: repeat(4, minmax(0, 1fr));
}
.flow-item {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 0.85rem 0.9rem;
}
.flow-item span {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 600;
}
.flow-item b { display: block; font-size: 0.88rem; margin: var(--space-2) 0 var(--space-1); }
.flow-item small { color: var(--muted); font-size: var(--text-xs); }

.app-footer {
    border-top: 1px solid var(--line);
    color: var(--muted);
    display: flex;
    flex-wrap: wrap;
    font-size: var(--text-xs);
    gap: var(--space-2) var(--space-5);
    justify-content: space-between;
    margin-top: var(--space-6);
    padding-top: var(--space-4);
}

/* ---------- Responsif ---------- */
/* Tablet: kolom Streamlit dibagi dua agar kartu tidak terlalu sempit. */
@media (max-width: 900px) {
    .flow-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .hero-title { font-size: 1.8rem; }
    /* Selector internal Streamlit: kolom horizontal. */
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 calc(50% - 0.5rem) !important;
        min-width: calc(50% - 0.5rem) !important;
    }
}

/* Smartphone: satu kolom, tombol penuh lebar, tabel bisa digulir. */
@media (max-width: 640px) {
    h1 { font-size: 1.65rem !important; }
    .block-container { padding-left: var(--space-4); padding-right: var(--space-4); }
    .hero-title { font-size: 1.6rem; }
    .hero-aside { padding: var(--space-4); }
    .quick-list { grid-template-columns: 1fr; }
    .peringkat-baris { grid-template-columns: 24px minmax(0, 1fr) 64px; }
    .peringkat-baris .peringkat-bar { display: none; }
    .aktivitas-baris { grid-template-columns: 38px minmax(0, 1fr); }
    .aktivitas-waktu { grid-column: 2; }
    .steps { flex-direction: column; }
    .step { border-bottom: 1px solid var(--line); border-right: 0; }
    .step:last-child { border-bottom: 0; }
    .gauge-wrap { align-items: flex-start; flex-direction: column; gap: var(--space-3); }
    .gauge { flex-basis: 104px; height: 104px; width: 104px; }
    .gauge::before { height: 82px; width: 82px; }
    .flow-list { grid-template-columns: 1fr; }
    .meta-row { align-items: flex-start; flex-direction: column; gap: 2px; }
    /* Selector internal Streamlit: kolom dan tombol. */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    /* Selector internal Streamlit: pembungkus tombol ikut penuh agar tombol
       tidak hanya melebar di dalam wadah yang masih menyempit. */
    [data-testid="stFormSubmitButton"],
    [data-testid="stDownloadButton"],
    [data-testid="stButton"] { width: 100% !important; }
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stDownloadButton"] button,
    [data-testid="stButton"] button { width: 100% !important; }
    [data-testid="stDataFrame"] { overflow-x: auto !important; }
    .app-footer { flex-direction: column; }
}

/* Pengguna yang memilih mengurangi animasi tetap mendapat tampilan yang sama. */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
"""

_LANGKAH = [
    ("Data", "Isi identitas"),
    ("Gejala", "Pilih keluhan"),
    ("Analisis", "Bandingkan kasus"),
    ("Hasil", "Tinjau & simpan"),
]

_MENU = {
    "Beranda": "01",
    "Cek Gejala": "02",
    "Riwayat": "03",
}

_TAHAPAN_CBR = [
    ("Retrieve", "Cari kasus paling mirip"),
    ("Reuse", "Pakai solusi kasus terdekat"),
    ("Revise", "Tinjau dan sesuaikan"),
    ("Retain", "Simpan sebagai pembanding"),
]


def terapkan_tema():
    """Memasang gaya visual sekali setiap kali aplikasi dijalankan ulang."""
    st.markdown(_CSS, unsafe_allow_html=True)


def label_menu(nama):
    """Menambahkan nomor kecil pada menu agar mudah dipindai."""
    nomor = _MENU.get(nama)
    return f"{nomor}   {nama}" if nomor else str(nama)


def sidebar_hero():
    """Identitas aplikasi di bagian atas sidebar."""
    return """
    <div class="brand">
        <div class="brand-mark">+</div>
        <div>
            <div class="brand-name">CEKDBD</div>
            <div class="brand-tag">sistem untuk mendeteksi gejala anda</div>
        </div>
    </div>
    """


def sidebar_info():
    """Catatan singkat di bawah navigasi."""
    return """
    <div class="side-note">
        <b>Metode</b><br>
        Cosine Similarity dihitung manual dengan Python dasar.<br><br>
        <b>Alur</b><br>
        Retrieve → Reuse → Revise → Retain
    </div>
    """


def header(judul, deskripsi, eyebrow=None):
    """Header halaman: eyebrow, judul, lalu satu paragraf pembuka."""
    if eyebrow:
        st.markdown(
            f'<div class="eyebrow">{escape(str(eyebrow))}</div>',
            unsafe_allow_html=True,
        )
    st.title(judul)
    st.markdown(
        f'<p class="lead">{escape(str(deskripsi))}</p>',
        unsafe_allow_html=True,
    )


def bagian(nomor, judul, keterangan=""):
    """Judul bagian dengan nomor kecil di atasnya."""
    if nomor:
        st.markdown(
            f'<div class="section-number">{escape(str(nomor))}</div>',
            unsafe_allow_html=True,
        )
    st.subheader(judul)
    if keterangan:
        st.caption(keterangan)


def judul_kartu(teks, besar=False):
    """Judul bergaya serif di dalam kartu, untuk nama kasus atau solusi."""
    kelas = "card-title lg" if besar else "card-title"
    st.markdown(
        f'<div class="{kelas}">{escape(str(teks))}</div>',
        unsafe_allow_html=True,
    )


def catatan(teks, peringatan=False):
    """Catatan kecil yang menenangkan, bukan alert berwarna mencolok."""
    kelas = "note note--warning" if peringatan else "note"
    st.markdown(
        f'<div class="{kelas}">{escape(str(teks))}</div>',
        unsafe_allow_html=True,
    )


def _status_info(persentase):
    """
    Menentukan status visual dari persentase kemiripan.

    Ambang 60% dipilih karena kasus contoh terbaik berada di sekitar 61,7%,
    sehingga hasil acuan tampil sebagai "Perlu perhatian". Status ini hanya
    menggambarkan kedekatan kasus, bukan diagnosis medis.
    """
    nilai = float(persentase or 0)
    if nilai >= 60:
        return "Perlu perhatian", "perhatian", "Kedekatan kasus tinggi"
    return "Aman", "aman", "Kedekatan kasus rendah"


def status_badge_html(persentase):
    """Menghasilkan HTML label status untuk dipakai di dalam kartu."""
    label, kelas, keterangan = _status_info(persentase)
    return (
        f'<span class="status-badge status-badge--{kelas}" '
        f'title="{escape(keterangan)}">{escape(label)}</span>'
    )


def status_badge(persentase):
    """Menampilkan label status kecil untuk persentase kemiripan."""
    st.markdown(
        f'<div class="gauge-badges">{status_badge_html(persentase)}</div>',
        unsafe_allow_html=True,
    )


def kosong(judul, deskripsi, petunjuk=None):
    """Empty state yang menjelaskan apa yang harus dilakukan pengguna."""
    isi = (
        '<div class="empty-state">'
        f'<div class="empty-title">{escape(str(judul))}</div>'
        f'<p class="empty-copy">{escape(str(deskripsi))}</p>'
    )
    if petunjuk:
        isi += f'<p class="empty-copy">{escape(str(petunjuk))}</p>'
    isi += "</div>"
    st.markdown(isi, unsafe_allow_html=True)


def meta_rows(baris):
    """
    Menghasilkan baris label → nilai untuk panel ringkasan.

    `baris` berisi pasangan `(label, nilai)`. Fungsi ini hanya merangkai HTML;
    pemanggil yang memasangnya dengan `unsafe_allow_html=True`.
    """
    bagian = []
    for label, nilai in baris:
        bagian.append(
            '<div class="meta-row">'
            f"<span>{escape(str(label))}</span>"
            f"<b>{escape(str(nilai))}</b>"
            "</div>"
        )
    return '<div class="meta-list">' + "".join(bagian) + "</div>"


def pil_ringkas(daftar, label=None):
    """Menampilkan gejala terpilih sebagai label-label kecil yang rapi."""
    if not daftar:
        return
    if label:
        st.markdown(
            f'<div class="card-kicker">{escape(str(label))}</div>',
            unsafe_allow_html=True,
        )
    isi = "".join(f'<span class="pill">{escape(str(x))}</span>' for x in daftar)
    st.markdown(f'<div class="pill-row">{isi}</div>', unsafe_allow_html=True)


def grup_gejala(judul):
    """Pembatas antar-kelompok gejala pada langkah 2 Cek Gejala."""
    st.markdown(
        f'<div class="gejala-grup-judul">{escape(str(judul))}</div>',
        unsafe_allow_html=True,
    )


def peringkas(baris):
    """
    Daftar kasus terdekat dengan batang kemiripan.

    `baris` berisi dict dengan `peringkat`, `nama`, `cosine`, dan `persentase`.
    """
    bagian = []
    for b in baris:
        persen = float(b.get("persentase", 0) or 0)
        lebar = max(2.0, min(100.0, persen))
        cosine = round(float(b.get("cosine", 0) or 0), 4)
        _label, kelas, _keterangan = _status_info(persen)
        bagian.append(
            '<div class="peringkat-baris">'
            f'<span class="peringkat-no">{escape(str(b.get("peringkat", "")))}</span>'
            f'<span class="peringkat-nama">{escape(str(b.get("nama", "")))}</span>'
            f'<div class="peringkat-bar" title="Cosine {cosine}">'
            f'<i class="{kelas}" style="width:{lebar:.1f}%"></i></div>'
            f'<span class="peringkat-nilai">{persen:.1f}%</span>'
            "</div>"
        )
    st.markdown(
        '<div class="peringkat-list">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def kartu_riwayat(id_konsultasi, nama, persentase, solusi, waktu):
    """Kartu ringkas satu pemeriksaan di halaman Riwayat."""
    _label, kelas, _keterangan = _status_info(persentase)
    st.markdown(
        '<div class="riwayat-kartu riwayat-kartu--' + kelas + '">'
        '<div class="riwayat-top">'
        '<div class="riwayat-identitas">'
        f'<div class="riwayat-id">#{escape(str(id_konsultasi))}</div>'
        f'<div class="riwayat-judul">{escape(str(nama))}</div>'
        "</div>"
        '<div class="riwayat-badges">'
        f'<div class="riwayat-nilai">{round(float(persentase), 1)}%'
        "<small> kemiripan</small></div>"
        f"{status_badge_html(persentase)}"
        "</div>"
        "</div>"
        '<div class="riwayat-meta">'
        f"<span><b>Solusi:</b> {escape(str(solusi))}</span>"
        f"<span><b>Dicatat:</b> {escape(str(waktu))}</span>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def aktivitas_ringkas(baris):
    """Daftar aktivitas terbaru tanpa tampilan tabel yang kaku."""
    bagian = []
    for b in baris:
        titik = ""
        if "persentase" in b:
            _label, kelas, keterangan = _status_info(b["persentase"])
            titik = (
                f'<span class="status-dot status-dot--{kelas}" '
                f'title="{escape(keterangan)}"></span>'
            )
        bagian.append(
            '<div class="aktivitas-baris">'
            f'<span class="aktivitas-id">#{escape(str(b.get("id", "")))}</span>'
            '<div class="aktivitas-isi">'
            f'<b>{escape(str(b.get("nama", "")))}{titik}</b>'
            f'<small>{escape(str(b.get("solusi", "")))}</small>'
            "</div>"
            f'<span class="aktivitas-waktu">{escape(str(b.get("waktu", "")))}</span>'
            "</div>"
        )
    st.markdown(
        '<div class="aktivitas-list">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def quick_steps():
    """Tiga langkah singkat di Beranda, tanpa ikon atau dekorasi berlebih."""
    data = [
        ("01", "Data pasien", "Identitas singkat"),
        ("02", "Pilih gejala", "Centang keluhan"),
        ("03", "Lihat hasil", "Bandingkan kasus"),
    ]
    bagian = []
    for nomor, judul, keterangan in data:
        bagian.append(
            '<div class="quick-item">'
            f"<span>{escape(nomor)}</span>"
            f"<b>{escape(judul)}</b>"
            f"<small>{escape(keterangan)}</small>"
            "</div>"
        )
    st.markdown(
        '<div class="quick-list">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def langkah_cbr(aktif):
    """
    Menampilkan empat langkah yang mudah dipahami pengguna.

    `aktif` bisa berisi "Data", "Gejala", "Analisis", atau "Hasil".
    """
    indeks_aktif = -1
    for i, (nama, _catatan) in enumerate(_LANGKAH):
        if nama == aktif:
            indeks_aktif = i

    bagian = []
    for i, (nama, catatan_step) in enumerate(_LANGKAH):
        if i == indeks_aktif:
            kelas = "aktif"
        elif indeks_aktif > i:
            kelas = "done"
        else:
            kelas = ""
        bagian.append(
            f'<div class="step {kelas}">'
            f'<span class="step-no">{i + 1:02d}</span>'
            f'<span class="step-name">{escape(nama)}</span>'
            f'<span class="step-note">{escape(catatan_step)}</span>'
            "</div>"
        )

    st.markdown(
        '<div class="steps">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def flow_cards():
    """Penjelasan singkat empat tahap CBR di halaman Beranda."""
    bagian = []
    for i, (nama, keterangan) in enumerate(_TAHAPAN_CBR):
        bagian.append(
            '<div class="flow-item">'
            f"<span>{i + 1:02d}</span>"
            f"<b>{escape(nama)}</b>"
            f"<small>{escape(keterangan)}</small>"
            "</div>"
        )
    st.markdown(
        '<div class="flow-list">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def kartu_ringkas(judul, nilai, petunjuk):
    """Kartu kecil untuk angka ringkasan."""
    st.markdown(
        '<div class="summary-card">'
        f'<div class="label">{escape(str(judul))}</div>'
        f'<div class="value">{escape(str(nilai))}</div>'
        f'<div class="hint">{escape(str(petunjuk))}</div>'
        "</div>",
        unsafe_allow_html=True,
    )


def gauge(persentase, nama_kasus, keterangan=""):
    """
    Cincin persentase kemiripan beserta status aman/perlu perhatian.

    Nilai sudah dihitung di core/cbr.py. Fungsi ini hanya menyesuaikan tampilan
    agar tetap berada di rentang 0–100 dan memberi label status visual.
    """
    nilai = float(persentase)
    if nilai < 0:
        nilai = 0.0
    if nilai > 100:
        nilai = 100.0
    derajat = round(nilai * 3.6, 1)
    label, kelas, keterangan_status = _status_info(nilai)
    ket = f'<div class="baris">{escape(str(keterangan))}</div>' if keterangan else ""

    st.markdown(
        '<div class="gauge-wrap">'
        f'<div class="gauge gauge--{kelas}" style="--derajat:{derajat}deg">'
        f'<div class="teks"><b>{round(nilai, 1)}%</b><br><small>kemiripan kasus</small></div>'
        "</div>"
        '<div class="gauge-info">'
        '<div class="label">Kasus pembanding</div>'
        f'<div class="nama">{escape(str(nama_kasus))}</div>'
        '<div class="gauge-badges">'
        f'<span class="status-badge status-badge--{kelas}" '
        f'title="{escape(keterangan_status)}">{escape(label)}</span>'
        "</div>"
        f"{ket}"
        "</div></div>",
        unsafe_allow_html=True,
    )


def footer():
    """Penutup halaman seperti pada website umumnya."""
    st.markdown(
        '<div class="app-footer">'
        "<span>CEKDBD · Sistem pendukung keputusan berbasis kasus</span>"
        "<span>Perhitungan Cosine Similarity dilakukan manual dengan Python dasar</span>"
        "</div>",
        unsafe_allow_html=True,
    )
