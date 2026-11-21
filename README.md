# SPK Berbasis Case-Based Reasoning (CBR) — Deteksi DBD

Aplikasi web dinamis untuk **Sistem Pendukung Keputusan** yang mengimplementasikan
metode **Case-Based Reasoning (CBR)** dengan pencarian kasus paling mirip memakai
**Cosine Similarity yang dihitung manual menggunakan Python dasar**.

> Seluruh perhitungan inti (dot product, panjang vektor, cosine similarity,
> penentuan kasus terdekat) ditulis sendiri dengan `for`, `if`, `def`,
> operator indeks, dan operasi aritmatika biasa.
> **Tidak ada NumPy / Pandas / Scikit-learn / SciPy** yang mengambil alih perhitungan.

---

## 1. Cara Menjalankan

Prasyarat: **Python 3.10 atau lebih baru**.

```bash
# 1. (Opsional) buat virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py
```

Browser otomatis terbuka di `http://localhost:8501`.

Database `spk_dbd.db` **dibuat otomatis** pada saat pertama kali aplikasi dijalankan,
lalu diisi 14 gejala DBD + 4 kasus contoh (vektor kasus contoh = `data_lama`
pada file `cbr.py`, sehingga hasilnya bisa langsung dibandingkan dengan kode acuan).

---

## 2. Menjalankan Pengujian

```bash
python -m unittest discover -s tests -v
```

Pengujian HTTP ke server yang benar-benar berjalan (opsional):

```bash
streamlit run app.py --server.port 8599 --server.enableAgentApi true
python uji_end_to_end.py spk_dbd.db 8599
```

Flag `--server.enableAgentApi true` wajib agar skrip bisa memakai endpoint
`/_stcore/agent/interact`. Karena menu sidebar memakai ikon lewat `format_func`,
skrip e2e membaca label tampilan (mis. `🩺 Konsultasi Baru`) melalui fungsi
`pilihan_menu()`, bukan nilai radio mentahnya.

47 pengujian mencakup: dot product, rincian perkalian, jumlah kuadrat,
panjang vektor, cosine similarity, vektor nol, jumlah atribut berbeda,
penentuan kasus terdekat, peringkat, CRUD database, validasi duplikat kode,
alur konsultasi lengkap (Retrieve → Reuse → Revise → Retain), pesan feedback
setelah `st.rerun()`, dan render setiap halaman lewat AppTest Streamlit.

---

## 3. Struktur Project

```
spk-db/
├── app.py                     # Entry point Streamlit + navigasi sidebar
├── cbr.py                     # KODE ACUAN dari dosen (tidak diubah)
│
├── core/                      # ===== PERHITUNGAN INTI (murni Python) =====
│   ├── cosine.py              #   dot product, panjang vektor, cosine similarity
│   └── cbr.py                 #   Retrieve, Reuse, Revise, Retain
│
├── services/                  # ===== DATABASE & VALIDASI =====
│   ├── database.py            #   koneksi, pembuatan tabel, data awal
│   ├── kriteria.py            #   CRUD kriteria/gejala
│   ├── kasus.py               #   CRUD kasus
│   ├── riwayat.py             #   simpan & baca riwayat konsultasi
│   └── validasi.py            #   aturan validasi form
│
├── ui/                        # ===== TAMPILAN (Streamlit) =====
│   ├── dashboard.py           #   ringkasan data + hasil terbaru
│   ├── konsultasi.py          #   4 tahap CBR + tampilan transparan
│   ├── kasus.py               #   manajemen kasus
│   ├── kriteria.py            #   manajemen kriteria
│   ├── riwayat.py             #   riwayat perhitungan
│   ├── tema.py                #   CSS, sidebar, header, gauge, badge, penanda CBR
│   └── helper.py              #   tabel, format angka, dan flash message
│
├── tests/                     # ===== PENGUJIAN =====
│   ├── test_perhitungan.py    #   unit test matematika CBR
│   ├── test_database.py       #   test database + alur lengkap
│   └── test_ui.py             #   test render + alur lewat AppTest
│
├── uji_end_to_end.py          # Uji HTTP ke server Streamlit yang berjalan
├── requirements.txt
└── DOKUMENTASI.md             # Dokumentasi lengkap untuk sidang
```

> `index.html`, `script.js`, dan `style.css` adalah berkas dari versi awal
> berbasis HTML statis. Aplikasi Streamlit **tidak membaca** ketiga berkas itu;
> seluruh antarmuka ada di folder `ui/`.

**Aturan pemisahan:** `core/` tidak boleh mengimpor Streamlit/database,
`ui/` tidak boleh memuat perhitungan, `services/` tidak boleh memuat perhitungan CBR.

---

## 4. Alur Aplikasi

```
User memilih gejala (form)
        │
        ▼
ui/konsultasi.py  ──►  core/cbr.py  ──►  core/cosine.py
   (form & tampilan)     (bangun vektor,     (rincian dot, dot product,
                          retrieve, reuse,     jumlah kuadrat, panjang vektor,
                          revise, retain)      cosine)
        │
        ▼
services/ (validasi)  ──►  services/database.py  ──►  spk_dbd.db
```

---

## 5. Fitur

| Halaman | Fitur |
|---|---|
| **Dashboard** | Tema modern, sidebar gelap, kartu metrik, gauge persentase, grafik kemiripan, kartu alur CBR, riwayat 5 konsultasi terakhir |
| **Konsultasi Baru** | Form berkartu, penanda 4 tahap, spinner, ringkasan kasus paling mirip, detail perkalian tiap gejala |
| **Manajemen Kasus** | Kartu ringkas, form berkartu, daftar kasus rapi; tambah, ubah, hapus kasus beserta solusi & gejala |
| **Manajemen Kriteria** | Dua kolom Tambah/Perbarui + kartu ringkas; proteksi kriteria yang sudah dipakai kasus |
| **Riwayat Perhitungan** | Kartu ringkas, gauge per konsultasi, detail dot product, panjang vektor, cosine, peringkat |

---

## 6. Library yang Digunakan

| Library | Alasan |
|---|---|
| **Streamlit** | Framework web Python paling sederhana untuk aplikasi dinamis; cukup fungsi Python biasa |
| **sqlite3** (bawaan Python) | Database relasional tanpa perlu instal server |
| **json** (bawaan Python) | Menyimpan vektor input pada riwayat |
| **unittest** (bawaan Python) | Pengujian tanpa library tambahan |

**Tidak digunakan:** NumPy, Pandas, Scikit-learn, SciPy, atau library otomatis lain
untuk perhitungan. (NumPy/Pandas hanya ikut terpasang sebagai dependensi internal
Streamlit untuk tampilan — kode project tidak mengimpornya.)

---

## 7. Dokumentasi Lengkap

Baca **[DOKUMENTASI.md](DOKUMENTASI.md)** untuk penjelasan arsitektur, rumus
Cosine Similarity, alur CBR, dan panduan menjelaskan project ke dosen.
