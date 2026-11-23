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

    /* Warna: stone hangat + pine gelap + teal + satu aksen tanah liat. */
    --bg: #f5f3ee;
    --surface: #ffffff;
    --surface-alt: #faf9f5;
    --surface-deep: #0d2e28;
    --surface-deep-2: #123c34;
    --ink: #12251f;
    --muted: #5f6b64;
    --line: #e1e3da;
    --line-soft: #eeefe9;
    --accent: #0d6b58;
    --accent-dark: #084b3e;
    --accent-soft: #e3f0ea;
    --accent-wash: #f2f7f3;
    --accent-bright: #8ed2bd;
    /* Teks di atas panel pine. */
    --deep-ink: #f4faf7;
    --deep-muted: #c5d7cf;
    --deep-line: rgba(255, 255, 255, 0.16);
    --gauge-track: #e8ebe5;
    /* Satu warna peringatan saja: clay, lebih hangat dari kuning atau merah. */
    --warning: #a5532e;
    --warning-dark: #7e3c20;
    --warning-soft: #fbede6;
    --warning-line: #ebd0c0;
    /* Turunan warna yang dipakai berulang. */
    --white: var(--surface);
    --focus: rgba(13, 107, 88, 0.22);
    --hover: #f0f2ec;
    --brand-mark-border: rgba(142, 210, 189, 0.45);
    --brand-mark-shadow: 0 6px 14px rgba(8, 76, 63, 0.30);
    --chip-bg: rgba(255, 255, 255, 0.07);
    --button-shadow: 0 6px 14px rgba(8, 76, 63, 0.18);
    /* Hero Beranda: palet yang ditentukan, dengan rasio kontras WCAG AA.
       Teks utama 11.93:1, teks sekunder 5.40:1, tombol putih 4.88:1. */
    --hero-bg: #e8f3ef;
    --hero-line: #0b8068;
    --hero-ink: #18332d;
    --hero-copy: #52665f;
    --hero-accent: #0b8068;
    --hero-accent-dark: #086b57;
    --hero-cream: #f8f7f2;
    --hero-focus: rgba(11, 128, 104, 0.32);

    /* Ruang */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
    --space-7: 2.75rem;

    /* Ukuran kotak yang dipakai bersama agar panel dan kartu seragam. */
    --panel-min-h: 350px;
    --panel-col-min-h: 300px;
    --card-min-h: 132px;

    /* Radius & bayangan: sengaja dikunci agar tidak terlihat seperti template. */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-pill: 999px;
    --shadow-sm: 0 1px 2px rgba(18, 37, 31, 0.06);
    --shadow-md: 0 12px 28px rgba(18, 37, 31, 0.10);
    --shadow-deep: 0 14px 32px rgba(13, 46, 40, 0.18);

    /* Tipografi */
    --font-ui: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    --font-display: Georgia, "Times New Roman", serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
    --text-xs: 0.78rem;
    --text-sm: 0.88rem;
    --text-md: 0.96rem;
    --text-lg: 1.12rem;
    --text-xl: 1.5rem;
    --text-2xl: 2rem;
}

/* ---------- Dasar ---------- */
html, body, [class*="css"] {
    font-family: var(--font-ui);
}
html, body {
    background: var(--bg) !important;
    color: var(--ink) !important;
}
/* Selector internal Streamlit: aplikasi root. `!important` diperlukan karena
   tema gelap Streamlit disuntikkan setelah gaya ini. */
[data-testid="stApp"] {
    background: var(--bg) !important;
    color-scheme: light only !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: var(--bg) !important;
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
    padding-top: 2.4rem;
    padding-bottom: var(--space-6);
}
/* Selector internal Streamlit: kolom dalam satu baris ikut merentang supaya
   panel di dalamnya bisa memiliki tinggi yang sama. */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { align-self: stretch; }
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div { height: 100%; }

h1 {
    color: var(--ink) !important;
    font-family: var(--font-display);
    font-size: var(--text-2xl) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
    margin: var(--space-2) 0 var(--space-3) !important;
}
h2 {
    color: var(--ink) !important;
    font-size: var(--text-lg) !important;
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
/* Selector internal Streamlit: sidebar, radio navigasi, dan konten user. */
[data-testid="stSidebar"] {
    background: var(--surface-alt) !important;
    border-right: 1px solid var(--line);
    color-scheme: light only;
}
[data-testid="stSidebar"] * { color: var(--ink) !important; }
[data-testid="stSidebarUserContent"] {
    padding: 0.9rem 0.9rem 1.1rem !important;
}

/* Identitas aplikasi: kartu pine kecil di puncak sidebar. */
.brand {
    background: var(--surface-deep);
    border: 1px solid var(--surface-deep-2);
    border-radius: var(--radius-lg);
    color: var(--deep-ink) !important;
    margin-bottom: var(--space-5);
    overflow: hidden;
    padding: var(--space-4);
    position: relative;
}
/* Garis atas pada kartu identitas dan panel ringkasan memakai geometri yang
   sama; warnanya sengaja dipisah supaya masing-masing mengikuti konteksnya. */
.brand::before,
.hero-aside::before {
    content: "";
    height: 3px;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
}
.brand::before { background: var(--accent-bright); }
.brand * { color: inherit !important; }
.brand-head { align-items: center; display: flex; gap: var(--space-3); }
.brand-mark {
    align-items: center;
    background: var(--accent);
    border: 1px solid var(--brand-mark-border);
    border-radius: 11px;
    box-shadow: var(--brand-mark-shadow);
    color: var(--white) !important;
    display: inline-flex;
    flex: 0 0 42px;
    font-family: var(--font-display);
    font-size: 1.65rem;
    height: 42px;
    justify-content: center;
    line-height: 1;
}
.brand-eyebrow {
    color: var(--accent-bright) !important;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.brand-name {
    color: var(--deep-ink) !important;
    font-family: var(--font-display);
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    line-height: 1.1;
    margin-top: 2px;
}
.brand-tag {
    border-top: 1px solid var(--deep-line);
    color: var(--deep-muted) !important;
    font-size: var(--text-xs);
    line-height: 1.5;
    margin-top: var(--space-3);
    padding-top: var(--space-3);
}
.brand-chips { display: flex; flex-wrap: wrap; gap: var(--space-2); margin-top: var(--space-3); }
.brand-chip {
    background: var(--chip-bg);
    border: 1px solid var(--deep-line);
    border-radius: var(--radius-pill);
    color: var(--deep-muted) !important;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.16rem 0.5rem;
    text-transform: uppercase;
}
.brand-chip:first-child { color: var(--accent-bright) !important; }

/* Navigasi: nomor dan nama dirender ulang lewat pseudo-element agar
   tetap rapi, tetapi nilai radio asli tidak diubah. */
[data-testid="stRadioGroup"]::before {
    color: var(--muted) !important;
    content: "MENU UTAMA";
    display: block;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    margin: 0 0 var(--space-2) var(--space-1);
}
/* Radio group Streamlit memakai flex column yang menyusut mengikuti panjang
   teks. Paksa stretch agar ketiga menu memakai lebar penuh sidebar, sehingga
   tepi kiri/kanan sejajar baik saat aktif maupun tidak aktif. */
[data-testid="stRadioGroup"] {
    align-items: stretch !important;
    box-sizing: border-box !important;
    width: 100% !important;
}
[data-testid="stRadioGroup"] > div {
    box-sizing: border-box !important;
    margin-bottom: var(--space-2);
    width: 100% !important;
}
[data-testid="stRadioOption"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    box-sizing: border-box !important;
    cursor: pointer;
    display: block;
    min-height: 3.125rem;
    padding: 0.6rem 0.7rem;
    transition: background 0.15s ease, border-color 0.15s ease,
                transform 0.15s ease;
    width: 100% !important;
}
[data-testid="stRadioOption"]:hover {
    border-color: var(--accent);
    transform: translateX(2px);
}
/* Sembunyikan indikator radio bawaan Streamlit. */
[data-testid="stRadioOption"] > div > div:first-child { display: none !important; }
[data-testid="stRadioOption"] [data-testid="stMarkdownContainer"] p {
    align-items: center;
    color: var(--ink) !important;
    display: flex;
    font-size: 0 !important;
    gap: var(--space-3);
    margin: 0;
}
[data-testid="stRadioOption"] [data-testid="stMarkdownContainer"] p::before {
    align-items: center;
    background: var(--surface-alt);
    border: 1px solid var(--line);
    border-radius: 9px;
    color: var(--muted) !important;
    content: "00";
    display: inline-flex;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 700;
    height: 28px;
    justify-content: center;
    letter-spacing: 0;
    width: 30px;
}
[data-testid="stRadioOption"] [data-testid="stMarkdownContainer"] p::after {
    color: var(--ink) !important;
    content: "Menu";
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
[data-testid="stRadioGroup"] > div:nth-child(1) p::before { content: "01"; }
[data-testid="stRadioGroup"] > div:nth-child(1) p::after { content: "Beranda"; }
[data-testid="stRadioGroup"] > div:nth-child(2) p::before { content: "02"; }
[data-testid="stRadioGroup"] > div:nth-child(2) p::after { content: "Cek Gejala"; }
[data-testid="stRadioGroup"] > div:nth-child(3) p::before { content: "03"; }
[data-testid="stRadioGroup"] > div:nth-child(3) p::after { content: "Riwayat"; }

[data-testid="stRadioOption"][data-selected="true"] {
    background: var(--accent-soft);
    border-color: var(--accent);
    box-shadow: inset 3px 0 0 var(--accent);
}
[data-testid="stRadioOption"][data-selected="true"] p::before {
    background: var(--accent);
    border-color: var(--accent);
    color: var(--white) !important;
}
[data-testid="stRadioOption"][data-selected="true"] p::after {
    color: var(--accent-dark) !important;
}
[data-testid="stRadioOption"]:focus-visible {
    box-shadow: 0 0 0 3px var(--focus);
    outline: none;
}
[data-testid="stSidebar"] hr { border-color: var(--line) !important; }
/* Label radio tetap ada di DOM untuk pembaca layar dan pengujian, tetapi
   tidak ditampilkan dua kali karena navigasi sudah punya kicker MENU UTAMA. */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    border: 0 !important;
    clip: rect(0, 0, 0, 0) !important;
    height: 1px !important;
    margin: -1px !important;
    overflow: hidden !important;
    padding: 0 !important;
    position: absolute !important;
    white-space: nowrap !important;
    width: 1px !important;
}

/* Kartu informasi kecil di bawah navigasi. */
.side-note {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    color: var(--muted) !important;
    font-size: var(--text-xs);
    line-height: 1.6;
    margin-top: var(--space-4);
    padding: var(--space-4);
}
.side-note-title {
    color: var(--accent-dark) !important;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}
.side-note-title--jarak { margin-top: var(--space-3); }
.side-note-copy { margin-top: var(--space-1); }

/* ---------- Header halaman ---------- */
.eyebrow {
    align-items: center;
    color: var(--accent-dark) !important;
    display: inline-flex;
    font-size: var(--text-xs);
    font-weight: 700;
    gap: var(--space-2);
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.eyebrow::before {
    background: var(--accent);
    border-radius: var(--radius-pill);
    content: "";
    height: 2px;
    width: 20px;
}
.lead {
    color: var(--muted) !important;
    font-size: var(--text-md);
    margin: var(--space-1) 0 var(--space-5);
    max-width: 74ch;
}
.section-number {
    background: var(--accent-wash);
    border: 1px solid var(--line);
    border-radius: var(--radius-pill);
    color: var(--accent-dark) !important;
    display: inline-block;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.12em;
    margin-bottom: var(--space-2);
    padding: 0.15rem 0.55rem;
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
    margin: var(--space-4) 0;
}

/* ---------- Permukaan, form, tabel ---------- */
/* Selector internal Streamlit: pada versi ini `st.container(border=True)`
   dirender sebagai `stVerticalBlock` dengan `data-test-wrap="false"`. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"] {
    background: var(--surface);
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-sm);
    box-sizing: border-box;
    min-height: var(--panel-min-h);
    padding: var(--space-5) !important;
}
/* Isi panel ikut merentang supaya tinggi minimum benar-benar terlihat. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"] > [data-testid="stLayoutWrapper"] {
    display: flex;
    flex: 1 1 auto;
    flex-direction: column;
}
/* Kolom utama di dalam panel memakai tinggi minimum yang sama, sehingga
   panel dua kolom tidak ada yang lebih pendek hanya karena isinya sedikit. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"] > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
    min-height: var(--panel-col-min-h);
}
/* Panel pembuka: hijau lembut dengan garis hijau utama, tanpa gradient.
   Semua aturan di sini hanya berlaku untuk panel yang memuat .hero-title. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) {
    background: var(--hero-bg) !important;
    border-color: var(--hero-line) !important;
    box-shadow: inset 0 3px 0 var(--hero-accent), var(--shadow-sm) !important;
    padding: var(--space-6) !important;
}
/* Label "Mulai dari sini" dibentuk sebagai pill kecil agar konsisten dengan
   penomor bagian, tanpa mengubah .card-kicker yang dipakai halaman lain.
   Kicker pada panel ringkasan gelap sengaja dikecualikan agar kontrasnya
   dijaga oleh aturan .hero-aside tersendiri. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) .card-kicker:not(.hero-aside .card-kicker) {
    background: var(--hero-cream);
    border: 1px solid var(--hero-line);
    border-radius: var(--radius-pill);
    color: var(--hero-accent-dark) !important;
    display: inline-flex;
    font-family: var(--font-ui);
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    margin-bottom: var(--space-4);
    padding: 0.28rem 0.7rem;
}
/* Keterangan singkat di bawah tombol mengikuti warna teks sekunder hero. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) [data-testid="stCaptionContainer"] p {
    color: var(--hero-copy) !important;
}
[data-testid="stForm"] {
    background: var(--surface-alt);
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md);
    padding: var(--space-5) !important;
}
[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: var(--ink) !important;
    font-weight: 700 !important;
}
[data-testid="stDataFrame"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    max-width: 100%;
    overflow-x: auto;
}
/* Notifikasi mengikuti palet aplikasi. Streamlit memakai `kind` pada baseweb;
   dua bentuk selector dipakai agar versi lama dan baru tetap tertimpa. */
[data-testid="stAlert"] {
    background: var(--accent-wash) !important;
    border: 1px solid var(--line) !important;
    border-left: 3px solid var(--accent) !important;
    border-radius: var(--radius-md) !important;
    color: var(--ink) !important;
    font-size: var(--text-sm);
}
[data-testid="stAlert"] > div { background: transparent !important; }
[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    color: inherit !important;
}
[data-testid="stAlert"] svg { color: var(--accent) !important; }
[data-testid="stAlert"]:has([kind="warning"]),
[data-testid="stAlert"]:has([kind="danger"]),
[data-testid="stAlert"]:has([kind="error"]),
[data-testid="stAlert"][kind="warning"],
[data-testid="stAlert"][kind="danger"],
[data-testid="stAlert"][kind="error"] {
    background: var(--warning-soft) !important;
    border-left-color: var(--warning) !important;
    color: var(--warning-dark) !important;
}
[data-testid="stAlert"]:has([kind="warning"]) svg,
[data-testid="stAlert"]:has([kind="danger"]) svg,
[data-testid="stAlert"]:has([kind="error"]) svg,
[data-testid="stAlert"][kind="warning"] svg,
[data-testid="stAlert"][kind="danger"] svg,
[data-testid="stAlert"][kind="error"] svg { color: var(--warning) !important; }
/* Spinner memakai primaryColor Streamlit secara default; paksa ke aksen tea. */
[data-testid="stSpinner"] svg {
    color: var(--accent) !important;
    stroke: var(--accent) !important;
}
[data-testid="stSpinner"] [data-testid="stSpinnerIcon"] {
    border-right-color: var(--accent) !important;
    border-top-color: var(--accent) !important;
}

/* Angka ringkasan dirangkai sebagai satu strip, bukan sekumpulan kartu.
   Widget st.metric tetap dipakai supaya nilai terbaca oleh tooling dan
   pembaca layar; hanya kulit visualnya yang disatukan di sini. */
[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {
    background: var(--line-soft);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    gap: 1px !important;
    overflow: hidden;
}
[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"] {
    background: var(--surface);
}
[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"]:not(:last-child) {
    border-right: 1px solid var(--line-soft);
}
div[data-testid="stMetric"] {
    background: transparent;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: var(--card-min-h);
    padding: var(--space-4);
}
div[data-testid="stMetricLabel"] p {
    color: var(--muted) !important;
    font-size: var(--text-sm) !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-family: var(--font-display);
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    font-variant-numeric: tabular-nums;
    line-height: 1.2;
}

/* ---------- Tombol ---------- */
/* Selector internal Streamlit: versi lama memakai `baseButton-*`, versi baru
   memakai `stBaseButton-*`. Form submit primary memakai testid
   `primaryFormSubmit`, jadi ikut dicakup supaya tidak jatuh ke merah bawaan. */
button[data-testid="baseButton-primary"],
button[data-testid="stBaseButton-primary"],
button[data-testid="baseButton-primaryFormSubmit"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: var(--accent-dark) !important;
    border: 1px solid var(--accent-dark) !important;
    border-radius: var(--radius-sm) !important;
    box-shadow: var(--button-shadow) !important;
    color: var(--white) !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em;
    min-height: 44px;
    padding: 0.6rem 1.15rem !important;
    transition: background 0.15s ease, transform 0.08s ease, box-shadow 0.15s ease;
}
/* Metrik form submit disamakan dengan tombol primary biasa. */
button[data-testid="baseButton-primaryFormSubmit"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    font-size: 0.9rem !important;
}
button[data-testid="baseButton-primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="baseButton-primaryFormSubmit"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: var(--surface-deep) !important;
    border-color: var(--surface-deep) !important;
    box-shadow: var(--shadow-md) !important;
}
button[data-testid="baseButton-primary"]:active,
button[data-testid="stBaseButton-primary"]:active,
button[data-testid="baseButton-primaryFormSubmit"]:active,
button[data-testid="stBaseButton-primaryFormSubmit"]:active { transform: translateY(1px); }
/* Tombol sedang memuat tetap paling mirip primary, tanpa bayangan/efek aktif. */
button[data-testid="baseButton-primary"]:disabled,
button[data-testid="stBaseButton-primary"]:disabled,
button[data-testid="baseButton-primaryFormSubmit"]:disabled,
button[data-testid="stBaseButton-primaryFormSubmit"]:disabled {
    background: var(--accent-soft) !important;
    border-color: var(--line) !important;
    box-shadow: none !important;
    color: var(--muted) !important;
    cursor: not-allowed;
    transform: none;
}
button[data-testid="baseButton-secondary"],
button[data-testid="stBaseButton-secondary"] {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
    min-height: 44px;
    transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}
button[data-testid="baseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent-dark) !important;
}
button[data-testid="baseButton-primary"]:focus-visible,
button[data-testid="stBaseButton-primary"]:focus-visible,
button[data-testid="baseButton-primaryFormSubmit"]:focus-visible,
button[data-testid="stBaseButton-primaryFormSubmit"]:focus-visible,
button[data-testid="baseButton-secondary"]:focus-visible,
button[data-testid="stBaseButton-secondary"]:focus-visible {
    box-shadow: 0 0 0 3px var(--focus) !important;
    outline: none;
}
/* Tombol ajakan di hero saja: teks putih di hijau utama (4.88:1), hover dan
   active memakai hijau gelap (6.46:1). Tombol halaman lain tidak terpengaruh. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) [data-testid="stButton"] button {
    background: var(--hero-accent) !important;
    border: 1px solid var(--hero-accent) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--white) !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    min-height: 46px !important;
    padding: 0.72rem 1.35rem !important;
    transition: background 0.18s ease, border-color 0.18s ease,
                box-shadow 0.18s ease, transform 0.12s ease !important;
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) [data-testid="stButton"] button:hover {
    background: var(--hero-accent-dark) !important;
    border-color: var(--hero-accent-dark) !important;
    box-shadow: 0 2px 6px rgba(8, 107, 87, 0.18) !important;
    transform: translateY(-1px);
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) [data-testid="stButton"] button:active {
    background: var(--hero-accent-dark) !important;
    border-color: var(--hero-accent-dark) !important;
    box-shadow: inset 0 2px 4px rgba(24, 51, 45, 0.20) !important;
    transform: translateY(1px);
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) [data-testid="stButton"] button:focus-visible {
    box-shadow: 0 0 0 6px var(--hero-focus) !important;
    outline: 2px solid var(--hero-accent-dark) !important;
    outline-offset: 3px;
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) [data-testid="stButton"] button:disabled {
    background: var(--hero-cream) !important;
    border-color: var(--hero-line) !important;
    box-shadow: none !important;
    color: var(--hero-copy) !important;
    cursor: not-allowed;
    outline: none;
    transform: none;
}
/* Tombol "Lanjut" pada langkah 1 Cek Gejala memakai palet yang sama persis
   dengan tombol "Mulai Pemeriksaan" di Beranda. Penanda .tombol-ajakan hanya
   jadi jangkar :has(), jadi aturan ini tidak menyentuh tombol lain di panel. */
.tombol-ajakan { display: none; }
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) [data-testid="stFormSubmitButton"] button,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="baseButton-primaryFormSubmit"],
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: var(--hero-accent) !important;
    border: 1px solid var(--hero-accent) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--white) !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    min-height: 46px !important;
    padding: 0.72rem 1.35rem !important;
    transition: background 0.18s ease, border-color 0.18s ease,
                box-shadow 0.18s ease, transform 0.12s ease !important;
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) [data-testid="stFormSubmitButton"] button:hover,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="baseButton-primaryFormSubmit"]:hover,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: var(--hero-accent-dark) !important;
    border-color: var(--hero-accent-dark) !important;
    box-shadow: 0 2px 6px rgba(8, 107, 87, 0.18) !important;
    transform: translateY(-1px);
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) [data-testid="stFormSubmitButton"] button:active,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="baseButton-primaryFormSubmit"]:active,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="stBaseButton-primaryFormSubmit"]:active {
    background: var(--hero-accent-dark) !important;
    border-color: var(--hero-accent-dark) !important;
    box-shadow: inset 0 2px 4px rgba(24, 51, 45, 0.20) !important;
    transform: translateY(1px);
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) [data-testid="stFormSubmitButton"] button:focus-visible,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="baseButton-primaryFormSubmit"]:focus-visible,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="stBaseButton-primaryFormSubmit"]:focus-visible {
    box-shadow: 0 0 0 6px var(--hero-focus) !important;
    outline: 2px solid var(--hero-accent-dark) !important;
    outline-offset: 3px;
}
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) [data-testid="stFormSubmitButton"] button:disabled,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="baseButton-primaryFormSubmit"]:disabled,
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.tombol-ajakan) button[data-testid="stBaseButton-primaryFormSubmit"]:disabled {
    background: var(--hero-cream) !important;
    border-color: var(--hero-line) !important;
    box-shadow: none !important;
    color: var(--hero-copy) !important;
    cursor: not-allowed;
    outline: none;
    transform: none;
}
/* ---------- Input & fokus ---------- */
/* Selector internal Streamlit: baseweb dipakai input/textarea/checkbox. */
[data-testid="stCheckbox"] label { cursor: pointer; }
[data-testid="stCheckbox"] label:hover {
    background: var(--hover);
    border-radius: var(--radius-sm);
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    border-radius: var(--radius-sm) !important;
    font-size: var(--text-md);
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder { color: var(--muted); }
[data-baseweb="input"],
[data-baseweb="textarea"] {
    background: var(--surface-alt) !important;
    border-color: var(--line) !important;
    border-radius: var(--radius-sm) !important;
}
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    background: var(--surface) !important;
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
/* Nomor langkah dan nomor peringkat memakai bentuk lingkaran yang sama. */
.step-no,
.peringkat-no {
    align-items: center;
    border: 1px solid var(--line);
    border-radius: 50%;
    display: inline-flex;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 700;
    justify-content: center;
}
.step-no {
    background: var(--surface-alt);
    color: var(--muted);
    height: 28px;
    letter-spacing: 0;
    width: 28px;
}
.step-name {
    display: block;
    font-size: 0.88rem;
    font-weight: 700;
    margin-top: var(--space-2);
}
.step-note {
    color: var(--muted);
    display: block;
    font-size: var(--text-xs);
    margin-top: 2px;
}
.step.done .step-no {
    background: var(--accent-soft);
    border-color: var(--accent);
    color: var(--accent-dark);
    font-size: 0;
}
.step.done .step-no::after { content: "✓"; font-size: var(--text-sm); }
.step.active { background: var(--accent-wash); }
.step.active .step-no {
    background: var(--accent);
    border-color: var(--accent);
    color: var(--white);
}
.step.active .step-name { color: var(--accent-dark); }
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
.status-badge {
    align-items: center;
    border: 1px solid transparent;
    border-radius: var(--radius-pill);
    display: inline-flex;
    font-size: var(--text-xs);
    font-weight: 700;
    gap: var(--space-1);
    letter-spacing: 0.01em;
    padding: 0.22rem 0.6rem;
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
    background: conic-gradient(
        var(--gauge-color) var(--derajat),
        var(--gauge-track) var(--derajat) 360deg
    );
    border-radius: 50%;
    box-shadow: 0 0 0 1px var(--line), var(--shadow-sm);
    display: flex;
    flex: 0 0 116px;
    height: 116px;
    justify-content: center;
    position: relative;
    width: 116px;
}
.gauge--aman { --gauge-color: var(--accent); }
.gauge--perhatian { --gauge-color: var(--warning); }
.gauge::before {
    background: var(--surface);
    border-radius: 50%;
    box-shadow: inset 0 0 0 1px var(--line-soft);
    content: "";
    height: 90px;
    position: absolute;
    width: 90px;
}
.gauge .teks { position: relative; text-align: center; z-index: 1; }
.gauge .teks b {
    color: var(--ink);
    font-family: var(--font-display);
    font-size: 1.5rem;
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
    color: var(--hero-ink);
    font-family: var(--font-display);
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.16;
    margin: 0 0 var(--space-3);
    max-width: 24ch;
    overflow-wrap: break-word;
}
.hero-copy {
    color: var(--hero-copy) !important;
    font-size: 0.98rem;
    line-height: 1.65;
    margin: 0 0 var(--space-5);
    max-width: 54ch;
}
/* Aturan p Streamlit lebih spesifik, jadi warna deskripsi hero dikunci ulang
   di sini agar benar-benar memakai token --hero-copy. */
[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) .hero-copy {
    color: var(--hero-copy) !important;
    font-family: var(--font-ui);
}
.hero-aside {
    background: var(--hero-accent-dark);
    border: 1px solid var(--hero-accent-dark);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    color: var(--hero-cream);
    height: 100%;
    overflow: hidden;
    padding: var(--space-5);
    position: relative;
}
.hero-aside::before { background: var(--hero-bg); }
.hero-aside .card-kicker {
    color: var(--hero-bg) !important;
    margin-bottom: var(--space-2);
}
/* Teks dan garis pada panel gelap memakai krem/hijau lembut agar tidak
   jatuh di bawah 4.5:1 terhadap hijau gelap. */
.hero-aside .meta-list--gelap .meta-row { border-bottom-color: rgba(248, 247, 242, 0.28) !important; }
.hero-aside .meta-list--gelap .meta-row span { color: var(--hero-bg) !important; }
.hero-aside .meta-list--gelap .meta-row b { color: var(--hero-cream) !important; }
.meta-list { margin: var(--space-1) 0 0; }
.meta-list--gelap .meta-row { border-bottom-color: var(--deep-line); }
.meta-list--gelap .meta-row span { color: var(--deep-muted); }
.meta-list--gelap .meta-row b { color: var(--deep-ink); }
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
    background: var(--accent-wash);
    border: 1px solid var(--line);
    border-radius: var(--radius-pill);
    color: var(--accent-dark);
    font-size: var(--text-sm);
    font-weight: 600;
    padding: 0.25rem 0.65rem;
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
    background: var(--accent-wash);
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
    box-sizing: border-box;
    min-height: var(--panel-min-h);
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
/* Baris peringkat dan aktivitas memakai kartu ringkas yang sama; hanya ukuran
   kolom dan padding yang berbeda karena isinya berbeda. */
.peringkat-baris,
.aktivitas-baris {
    align-items: center;
    background: var(--surface-alt);
    border: 1px solid var(--line-soft);
    border-radius: var(--radius-md);
    display: grid;
    gap: var(--space-3);
    transition: background 0.15s ease, border-color 0.15s ease;
}
.peringkat-baris {
    font-size: var(--text-sm);
    grid-template-columns: 28px minmax(0, 1fr) 110px 72px;
    padding: 0.55rem 0.7rem;
}
.peringkat-baris:hover { background: var(--accent-wash); border-color: var(--line); }
.peringkat-no {
    background: var(--surface);
    color: var(--accent-dark);
    height: 24px;
    width: 24px;
}
.peringkat-nama { min-width: 0; overflow-wrap: anywhere; }
.peringkat-bar { background: var(--gauge-track); border-radius: var(--radius-pill); height: 6px; overflow: hidden; }
.peringkat-bar i { background: var(--accent); display: block; height: 100%; }
.peringkat-bar i.perhatian { background: var(--warning); }
.peringkat-nilai { font-variant-numeric: tabular-nums; font-weight: 700; text-align: right; }

.aktivitas-baris {
    grid-template-columns: 52px minmax(0, 1fr) auto;
    padding: 0.65rem 0.7rem;
}
.aktivitas-baris:hover { background: var(--accent-wash); border-color: var(--line); }
.aktivitas-id {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-pill);
    color: var(--accent-dark);
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 700;
    padding: 0.15rem 0.4rem;
    text-align: center;
}
.aktivitas-isi b { display: block; font-size: 0.9rem; }
.aktivitas-isi small { color: var(--muted); display: block; font-size: var(--text-xs); }
.aktivitas-waktu { color: var(--muted); font-size: var(--text-xs); white-space: nowrap; }

/* Alur singkat memakai rel langkah, bukan tiga kartu seragam. */
.process-rail {
    display: grid;
    gap: var(--space-4);
    grid-template-columns: repeat(3, minmax(0, 1fr));
    margin: var(--space-2) 0;
}
.process-step { border-top: 2px solid var(--line); padding-top: var(--space-3); }
.process-no {
    color: var(--accent-dark);
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 700;
    letter-spacing: 0.12em;
}
.process-step b { display: block; font-size: var(--text-md); margin-top: var(--space-1); }
.process-step small { color: var(--muted); font-size: var(--text-sm); }

/* ---------- Kelompok gejala & kartu riwayat ---------- */
.gejala-grup-judul {
    align-items: center;
    border-top: 1px solid var(--line-soft);
    color: var(--accent-dark) !important;
    display: flex;
    flex-wrap: wrap;
    font-size: var(--text-xs);
    font-weight: 700;
    gap: var(--space-2);
    letter-spacing: 0.12em;
    margin: var(--space-4) 0 var(--space-3);
    padding-top: var(--space-3);
    text-transform: uppercase;
}
.grup-jumlah {
    background: var(--accent-wash);
    border: 1px solid var(--line);
    border-radius: var(--radius-pill);
    color: var(--muted);
    font-size: var(--text-xs);
    letter-spacing: 0;
    padding: 0.1rem 0.45rem;
    text-transform: none;
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
    box-sizing: border-box;
    margin-bottom: var(--space-3);
    min-height: var(--card-min-h);
    padding: var(--space-4);
    transition: background 0.15s ease;
}
.riwayat-kartu:hover { background: var(--surface-alt); }
.riwayat-kartu--perhatian:hover { background: var(--warning-soft); }
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

/* Cara kerja dibaca sebagai urutan, bukan empat kartu dengan bentuk sama. */
.method-sequence { margin: var(--space-2) 0; }
.method-row {
    align-items: baseline;
    border-bottom: 1px solid var(--line-soft);
    display: grid;
    gap: var(--space-4);
    grid-template-columns: 46px minmax(150px, 0.55fr) minmax(0, 1.45fr);
    padding: var(--space-3) 0;
}
.method-row:first-child { padding-top: 0; }
.method-row:last-child { border-bottom: 0; padding-bottom: 0; }
.method-no {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: var(--text-sm);
    font-weight: 700;
}
.method-row b { font-family: var(--font-display); font-size: 1.08rem; }
.method-row small { color: var(--muted); font-size: var(--text-sm); }

.app-footer {
    background: var(--surface-alt);
    border: 1px solid var(--line);
    border-radius: var(--radius-lg);
    color: var(--muted);
    display: flex;
    flex-wrap: wrap;
    font-size: var(--text-xs);
    gap: var(--space-2) var(--space-5);
    justify-content: space-between;
    margin-top: var(--space-7);
    padding: var(--space-4) var(--space-5);
}
.app-footer span:first-child { color: var(--ink); font-weight: 700; }

/* ---------- Responsif ---------- */
/* Tablet: kolom Streamlit dibagi dua agar konten tidak terlalu sempit. */
@media (max-width: 900px) {
    .hero-title { font-size: 1.7rem; }
    [data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) {
        padding: var(--space-5) !important;
    }
    .process-rail { gap: var(--space-3); }
    /* Selector internal Streamlit: kolom horizontal. */
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 calc(50% - 0.5rem) !important;
        min-width: calc(50% - 0.5rem) !important;
    }
    /* Strip angka: 4 kolom menjadi 2×2, 3 kolom menjadi 2 + 1 penuh. */
    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"]:nth-child(odd):not(:last-child) {
        border-bottom: 1px solid var(--line-soft);
    }
    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"]:last-child:nth-child(odd) {
        flex-basis: 100% !important;
        min-width: 100% !important;
    }
}

/* Smartphone: satu kolom, tombol penuh lebar, tabel bisa digulir. */
@media (max-width: 640px) {
    h1 { font-size: 1.65rem !important; }
    .block-container { padding-left: var(--space-4); padding-right: var(--space-4); }
    .hero-title { font-size: 1.55rem; max-width: none; }
    [data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"][data-test-wrap="false"]:has(.hero-title) {
        padding: var(--space-4) !important;
    }
    .hero-aside { padding: var(--space-4); }
    .process-rail { grid-template-columns: 1fr; }
    .method-row { grid-template-columns: 34px minmax(0, 1fr); gap: var(--space-2) var(--space-3); }
    .method-row small { grid-column: 2; }
    .peringkat-baris { grid-template-columns: 24px minmax(0, 1fr) 64px; }
    .peringkat-baris .peringkat-bar { display: none; }
    .aktivitas-baris { grid-template-columns: 38px minmax(0, 1fr); }
    .aktivitas-waktu { grid-column: 2; }
    .steps { flex-direction: column; }
    .step { border-bottom: 1px solid var(--line); border-right: 0; }
    .step:last-child { border-bottom: 0; }
    .gauge-wrap { align-items: flex-start; flex-direction: column; gap: var(--space-3); }
    .gauge { flex-basis: 106px; height: 106px; width: 106px; }
    .gauge::before { height: 82px; width: 82px; }
    .meta-row { align-items: flex-start; flex-direction: column; gap: 2px; }
    .riwayat-badges { justify-content: space-between; width: 100%; }
    /* Selector internal Streamlit: kolom dan tombol. */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"] { border-bottom: 0 !important; }
    /* Selector internal Streamlit: pembungkus tombol ikut penuh agar tombol
       tidak hanya melebar di dalam wadah `width="fit-content"`. */
    [data-testid="stFormSubmitButton"],
    [data-testid="stDownloadButton"],
    [data-testid="stButton"],
    [data-testid="stElementContainer"]:has([data-testid="stButton"]),
    [data-testid="stElementContainer"]:has([data-testid="stFormSubmitButton"]),
    [data-testid="stElementContainer"]:has([data-testid="stDownloadButton"]) {
        width: 100% !important;
    }
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
        transform: none !important;
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
        <div class="brand-head">
            <div class="brand-mark">+</div>
            <div>
                <div class="brand-eyebrow">Sistem pakar</div>
                <div class="brand-name">CEKDBD</div>
            </div>
        </div>
        <div class="brand-tag">sistem untuk mendeteksi gejala anda</div>
        <div class="brand-chips">
            <span class="brand-chip">CBR</span>
            <span class="brand-chip">Cosine similarity</span>
        </div>
    </div>
    """


def sidebar_info():
    """Petunjuk singkat di bawah navigasi, bukan jargon teknis."""
    return """
    <div class="side-note">
        <div class="side-note-title">Cara pakai</div>
        <div class="side-note-copy">Isi identitas, pilih gejala, lalu baca perbandingan kasusnya.</div>
        <div class="side-note-title side-note-title--jarak">Yang perlu diingat</div>
        <div class="side-note-copy">Hasilnya membantu membaca kemungkinan, bukan diagnosis medis final.</div>
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


def kicker(teks):
    """Label kecil di atas judul kartu atau daftar."""
    st.markdown(
        f'<div class="card-kicker">{escape(str(teks))}</div>',
        unsafe_allow_html=True,
    )


def pemisah():
    """Garis pemisah antar-bagian dengan ritme yang sama di semua halaman."""
    st.markdown('<hr class="hairline">', unsafe_allow_html=True)


def stat_strip(data):
    """
    Merangkai angka ringkasan sebagai satu strip.

    `data` berisi pasangan `(label, nilai, petunjuk)`. Widget `st.metric`
    tetap dipakai supaya nilai terbaca oleh pembaca layar dan tooling;
    CSS di atas yang menyatukan tampilannya.
    """
    kolom = st.columns(len(data))
    for kol, item in zip(kolom, data):
        label, nilai, petunjuk = item
        with kol:
            st.metric(str(label), nilai, help=str(petunjuk))


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

    Ambang 60% dipilih karena kasus contoh terbaik berada di sekitar 61,7%.
    Label sengaja memakai "Rendah"/"Tinggi" agar tidak terdengar seperti
    penegasan medis; nilainya hanya kedekatan antar-kasus.
    """
    nilai = float(persentase or 0)
    if nilai >= 60:
        return "Tinggi", "perhatian", "Kedekatan kasus tinggi"
    return "Rendah", "aman", "Kedekatan kasus rendah"


def _status_kelas(persentase):
    """Mengambil kelas warna status tanpa memakai label dan keterangannya."""
    return _status_info(persentase)[1]


def status_badge_html(persentase):
    """Menghasilkan HTML label status untuk dipakai di dalam kartu."""
    label, kelas, keterangan = _status_info(persentase)
    return (
        f'<span class="status-badge status-badge--{kelas}" '
        f'role="img" aria-label="{escape(keterangan)}" '
        f'title="{escape(keterangan)}">{escape(label)}</span>'
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


def meta_rows(baris, gelap=False):
    """
    Menghasilkan baris label → nilai untuk panel ringkasan.

    `baris` berisi pasangan `(label, nilai)`. Set `gelap=True` untuk panel
    pine supaya warna teks dan garis mengikuti palet terang di atas gelap.
    Fungsi ini hanya merangkai HTML; pemanggil yang memasangnya dengan
    `unsafe_allow_html=True`.
    """
    bagian = []
    for label, nilai in baris:
        bagian.append(
            '<div class="meta-row">'
            f"<span>{escape(str(label))}</span>"
            f"<b>{escape(str(nilai))}</b>"
            "</div>"
        )
    kelas = "meta-list meta-list--gelap" if gelap else "meta-list"
    return f'<div class="{kelas}">' + "".join(bagian) + "</div>"


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


def grup_gejala(judul, jumlah=None):
    """Pembatas antar-kelompok gejala pada langkah 2 Cek Gejala."""
    jumlah_html = ""
    if jumlah is not None:
        jumlah_html = f'<span class="grup-jumlah">{escape(str(jumlah))} gejala</span>'
    st.markdown(
        '<div class="gejala-grup-judul">'
        f"<span>{escape(str(judul))}</span>"
        f"{jumlah_html}"
        "</div>",
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
        kelas = _status_kelas(persen)
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
    kelas = _status_kelas(persentase)
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
    """Tiga langkah singkat di Beranda, dirangkai sebagai rel proses."""
    data = [
        ("01", "Data pasien", "Identitas singkat"),
        ("02", "Pilih gejala", "Centang keluhan"),
        ("03", "Lihat hasil", "Bandingkan kasus"),
    ]
    bagian = []
    for nomor, judul, keterangan in data:
        bagian.append(
            '<div class="process-step">'
            f'<span class="process-no">{escape(nomor)}</span>'
            f"<b>{escape(judul)}</b>"
            f"<small>{escape(keterangan)}</small>"
            "</div>"
        )
    st.markdown(
        '<div class="process-rail">' + "".join(bagian) + "</div>",
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
    """Penjelasan empat tahap CBR sebagai urutan, bukan kartu seragam."""
    bagian = []
    for i, (nama, keterangan) in enumerate(_TAHAPAN_CBR):
        bagian.append(
            '<div class="method-row">'
            f'<span class="method-no">{i + 1:02d}</span>'
            f"<b>{escape(nama)}</b>"
            f"<small>{escape(keterangan)}</small>"
            "</div>"
        )
    st.markdown(
        '<div class="method-sequence">' + "".join(bagian) + "</div>",
        unsafe_allow_html=True,
    )


def gauge(persentase, nama_kasus, keterangan=""):
    """
    Cincin persentase kemiripan beserta label kedekatan rendah/tinggi.

    Nilai sudah dihitung di core/cbr.py. Fungsi ini hanya menyesuaikan tampilan
    agar tetap berada di rentang 0–100 dan memberi label status visual.
    """
    nilai = float(persentase)
    if nilai < 0:
        nilai = 0.0
    if nilai > 100:
        nilai = 100.0
    derajat = round(nilai * 3.6, 1)
    kelas = _status_kelas(nilai)
    ket = f'<div class="baris">{escape(str(keterangan))}</div>' if keterangan else ""

    st.markdown(
        '<div class="gauge-wrap">'
        f'<div class="gauge gauge--{kelas}" style="--derajat:{derajat}deg">'
        f'<div class="teks"><b>{round(nilai, 1)}%</b><br><small>kemiripan kasus</small></div>'
        "</div>"
        '<div class="gauge-info">'
        '<div class="label">Kasus pembanding</div>'
        f'<div class="nama">{escape(str(nama_kasus))}</div>'
        f'<div class="gauge-badges">{status_badge_html(nilai)}</div>'
        f"{ket}"
        "</div></div>",
        unsafe_allow_html=True,
    )


def footer():
    """Penutup halaman, disembunyikan saat pengguna masih mengisi wizard."""
    if (
        st.session_state.get("halaman_tujuan") == "Cek Gejala"
        and st.session_state.get("tahap_konsultasi", "Data") in ("Data", "Gejala")
    ):
        return
    st.markdown(
        '<div class="app-footer">'
        "<span>CEKDBD · Sistem pendukung keputusan berbasis kasus</span>"
        "<span>Perhitungan Cosine Similarity dilakukan manual dengan Python dasar</span>"
        "</div>",
        unsafe_allow_html=True,
    )
