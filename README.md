# CEKDBD — Sistem untuk mendeteksi gejala anda

Aplikasi web untuk pemeriksaan gejala DBD berbasis **Case-Based Reasoning (CBR)**.
Pengguna mengisi data singkat, memilih gejala, lalu melihat kasus paling mirip
memakai **Cosine Similarity yang dihitung manual dengan Python dasar**.

> Seluruh perhitungan inti (dot product, panjang vektor, cosine similarity,
> penentuan kasus terdekat) ditulis sendiri dengan `for`, `if`, `def`,
> operator indeks, dan operasi aritmatika biasa.
> **Tidak ada NumPy / Pandas / Scikit-learn / SciPy** yang mengambil alih perhitungan.

Tampilannya memakai design system tunggal di `ui/tema.py`: token warna, tipografi,
ruang, radius, dan bayangan. Tiga halamannya memakai komponen yang sama agar
konsisten di desktop, tablet, dan smartphone. Mode terang dipaksa walaupun
perangkat memakai tema gelap.

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
`/_stcore/agent/interact`. Menu sidebar memakai penomoran lewat `format_func`,
sehingga skrip e2e membaca label tampilan (mis. `02   Cek Gejala`) melalui
fungsi `pilihan_menu()`, bukan nilai radio mentahnya.

51 pengujian mencakup: dot product, rincian perkalian, jumlah kuadrat,
panjang vektor, cosine similarity, vektor nol, jumlah atribut berbeda,
penentuan kasus terdekat, peringkat, CRUD database, validasi, alur pemeriksaan
lengkap (Retrieve → Reuse → Revise → Retain), identitas CEKDBD, tombol
perpindahan menu, dan render setiap halaman lewat AppTest Streamlit.

---

## 3. Struktur Project

```
CekDBD/
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
│   ├── dashboard.py           #   Beranda + jalan masuk ke pemeriksaan
│   ├── konsultasi.py          #   Cek Gejala: data → gejala → hasil → tinjau → simpan
│   ├── riwayat.py             #   arsip pemeriksaan + kartu rincian
│   ├── tema.py                #   design system, brand, stepper, gauge, kartu
│   ├── helper.py              #   tabel dan format angka untuk tampilan
│   └── bantuan.py             #   komponen bersama + callback navigasi
│
├── assets/
│   └── favicon.svg            #   Ikon tab browser
│
├── laporan_assets/
│   └── diagram_alur_cekdbd.png
│
├── tests/                     # ===== PENGUJIAN =====
│   ├── test_perhitungan.py    #   unit test matematika CBR
│   ├── test_database.py       #   test database + alur lengkap
│   └── test_ui.py             #   test render + alur lewat AppTest
│
├── uji_end_to_end.py          # Uji HTTP ke server Streamlit yang berjalan
├── Laporan_Praktikum_SPK_CekDBD_Rakha.docx
├── DOKUMENTASI.md             # Dokumentasi lengkap untuk sidang
├── requirements.txt
└── .gitignore
```

> Halaman manajemen kasus dan kriteria sengaja tidak disertakan. Data awal
> (gejala dan kasus pembanding) tetap dibuat otomatis oleh `services/database.py`
> supaya pemeriksaan langsung bisa digunakan.

> Prototipe HTML statis lama (`index.html`, `script.js`, `style.css`) dan workflow
> GitHub Pages yang hanya menyajikan prototipe itu sudah dihapus. Seluruh
> antarmuka kini ada di folder `ui/`, dengan gaya visual terpusat di `ui/tema.py`.

**Aturan pemisahan:** `core/` tidak boleh mengimpor Streamlit/database,
`ui/` tidak boleh memuat perhitungan, `services/` tidak boleh memuat perhitungan CBR.

---

## 4. Alur Aplikasi

```
User membuka "Cek Gejala"
        │
        ▼
Isi data pasien → Lanjut → pilih gejala → Periksa Sekarang
        │
        ▼
ui/konsultasi.py  ──►  core/cbr.py  ──►  core/cosine.py
   (form & hasil)        (bangun vektor,     (rincian dot, dot product,
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
| **Beranda** | Tombol mulai pemeriksaan, ringkasan sistem, hasil terakhir, tiga kasus terdekat, penjelasan alur CBR |
| **Cek Gejala** | Alur dua langkah (data → gejala), gejala dua kolom dikelompokkan, stepper, label gejala terpilih, hasil dengan gauge dan status, tiga kasus terdekat, rincian perhitungan, tinjau solusi, simpan hasil, serta **Ubah Gejala** / **Pemeriksaan Baru** |
| **Riwayat** | Pencarian pemeriksaan, ekspor ringkasan CSV, kartu pemeriksaan dengan persentase dan status, rincian perbandingan, serta audit dot product/panjang vektor/cosine per kasus |

Tampilan sengaja dibuat tenang: tanpa emoji berlebihan, tanpa gradien generik,
dengan tipografi yang jelas dan ruang kosong yang cukup. Warna, font, radius,
dan bayangan didefinisikan sebagai design token di `ui/tema.py`, sehingga
perubahan desain cukup dilakukan di satu tempat. Status fokus, tombol utama,
dan tata letak responsif juga sudah disempurnakan untuk desktop, tablet, dan
ponsel. Beranda memakai headline editorial dengan ringkasan sistem, Cek Gejala
memisahkan input data dan gejala menjadi dua langkah serta menampilkan gejala
terpilih sebagai label kecil, dan Riwayat dapat dicari, diekspor ke CSV, serta
dipindai lewat kartu ringkas sebelum membuka rincian angka.
Perhitungan tetap transparan dan bisa dijelaskan baris per baris.

---

## 6. Library yang Digunakan

| Library | Alasan |
|---|---|
| **Streamlit ≥1.50** | Framework web Python paling sederhana untuk aplikasi dinamis; versi ini diperlukan untuk `st.html()` dan `st.dataframe(width=...)` |
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

Laporan praktikum tersedia dalam versi
**[DOCX](Laporan_Praktikum_SPK_CekDBD_Rakha.docx)**. Sumber diagram alurnya ada
di `laporan_assets/diagram_alur_cekdbd.png`.
