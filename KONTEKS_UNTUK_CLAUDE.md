# Konteks Source Code — CEKDBD

File ini dibuat sebagai panduan konteks untuk analisis UI/UX. Isi paket ZIP
sudah dipindahkan ke folder project dan diselaraskan dengan penyempurnaan
UI/UX terbaru.

## 1. Ringkasan teknologi

- **Bahasa utama:** Python 3.10+
- **Framework antarmuka:** Streamlit (`streamlit>=1.40`)
- **Database:** SQLite via modul bawaan `sqlite3`
- **Perhitungan:** Python murni (`math`), tanpa NumPy/Pandas/scikit-learn/SciPy
  untuk komputasi CBR maupun Cosine Similarity
- **Styling:** CSS yang disuntikkan lewat `st.markdown(..., unsafe_allow_html=True)`
  di `ui/tema.py`; bukan file CSS eksternal untuk aplikasi Streamlit. Warna,
  font, radius, dan bayangan memakai design token di `:root`
- **Testing:** `unittest` bawaan Python + Streamlit `AppTest`
- **Tidak ada:** Blade, PHP, `composer.json`, `package.json`, bundler frontend,
  atau build step untuk aplikasi utama

## 2. Struktur dan alur project

```
CEKDBD/
├── app.py                     # Entry point Streamlit, setup halaman, sidebar, navigasi
├── cbr.py                     # Kode acuan dosen (pembanding hasil)
├── requirements.txt           # Dependensi: Streamlit
├── README.md                  # Dokumentasi pengguna
├── DOKUMENTASI.md             # Dokumentasi teknis + alur + pengujian
├── uji_end_to_end.py          # Uji HTTP lewat Streamlit Agent API
├── .gitignore                 # Pengecualian __pycache__, *.pyc, *.db, .streamlit/
├── core/
│   ├── cosine.py              # dot product, jumlah kuadrat, panjang vektor, cosine
│   └── cbr.py                 # Retrieve, Reuse, Revise, Retain
├── services/
│   ├── database.py            # Koneksi SQLite, tabel, data awal
│   ├── kriteria.py            # CRUD gejala/kriteria + urutan vektor
│   ├── kasus.py               # CRUD kasus pembanding
│   ├── riwayat.py             # Simpan/baca riwayat + detail perbandingan
│   └── validasi.py            # Validasi input
├── ui/
│   ├── tema.py                # Design system, brand, stepper, gauge, kartu, footer
│   ├── helper.py              # Format tabel/angka untuk tampilan
│   ├── dashboard.py           # Halaman Beranda
│   ├── konsultasi.py          # Halaman Cek Gejala (alur utama)
│   └── riwayat.py             # Halaman Riwayat
└── tests/
    ├── test_perhitungan.py    # Unit test matematika CBR
    ├── test_database.py       # Test database + validasi + alur data
    └── test_ui.py             # Test antarmuka dengan AppTest
```

### Alur pengguna saat ini

1. `app.py` memuat tema, menginisialisasi database, lalu merender sidebar:
   `01 Beranda`, `02 Cek Gejala`, `03 Riwayat`.
2. Beranda menampilkan CTA **Mulai Pemeriksaan**, kartu metrik, hasil terakhir
   dengan gauge dan status, tiga kasus terdekat, aktivitas, dan penjelasan CBR.
3. Cek Gejala menjalankan alur bertahap sesuai `files.zip`: isi data →
   **Lanjut** → pilih gejala yang dikelompokkan (`Keluhan umum` dan
   `Tanda lanjutan`) → **Periksa Sekarang** → hasil/gauge → tiga kasus terdekat
   → rincian perhitungan → **Simpan Koreksi** → **Simpan Hasil Pemeriksaan**
   → **Ubah Gejala** / **Pemeriksaan Baru**.
4. Riwayat menampilkan pencarian, ekspor CSV, kartu pemeriksaan yang mudah
   dipindai, lalu rincian dan audit angka per kasus.
5. Navigasi dari tombol memakai `on_click` yang mengubah `st.session_state['halaman_tujuan']`,
   bukan menulis langsung radio setelah widget dibuat.

> `files.zip` berisi `CEKDBD_Alur_Bertahap.zip` dan
> `perubahan_alur_bertahap.patch`. Alur bertahapnya sudah diselaraskan ke
> `ui/konsultasi.py`, `tests/test_ui.py`, dan `uji_end_to_end.py`, sementara
> desain editorial proyek tetap dipertahankan.

## 3. File paling relevan untuk UI/UX

| Kategori | File |
|---|---|
| Entry point & navigasi | `app.py` |
| Styling/desain sistem | `ui/tema.py` |
| Layout halaman Beranda | `ui/dashboard.py` |
| Layout & interaksi halaman utama | `ui/konsultasi.py` |
| Layout halaman Riwayat | `ui/riwayat.py` |
| Komponen tabel dan format angka | `ui/helper.py` |
| Kontrak data/input yang dipakai form | `services/kriteria.py`, `services/validasi.py` |
| Data hasil yang ditampilkan UI | `services/kasus.py`, `services/riwayat.py`, `services/database.py` |
| Angka yang ditampilkan UI | `core/cosine.py`, `core/cbr.py` |
| Perilaku UI yang diuji | `tests/test_ui.py`, `uji_end_to_end.py` |
| Konteks produk & alur | `README.md`, `DOKUMENTASI.md` |
| Dependensi | `requirements.txt` |

> Catatan: prototipe statis lama (`index.html`, `script.js`, `style.css`) dan
> workflow GitHub Pages yang hanya menyajikan prototipe itu sudah dihapus dari
> project. Styling aktif seluruhnya ada di `ui/tema.py`.

## 4. Yang sengaja tidak disertakan

| Item | Alasan |
|---|---|
| `.git/` | Riwayat VCS bukan source code aplikasi; tidak diperlukan sebagai konteks UI/UX |
| `__pycache__/`, `*.pyc` | Hasil kompilasi Python, bukan source |
| `spk_dbd.db` | Database runtime yang dibuat otomatis; dapat diregenerasi oleh `services/database.py` |
| `ui/kasus.py`, `ui/kriteria.py` | Sudah dihapus dari aplikasi saat ini; menu manajemen tidak lagi dipakai |
| `index.html`, `script.js`, `style.css`, `.github/workflows/pages.yml` | Prototipe statis lama dan deploy Pages-nya sudah dihapus; aplikasi murni Streamlit |
| `.env`, API key, token, password, kredensial | Tidak ditemukan di project dan tidak boleh dimasukkan |
| `vendor/`, `node_modules/`, `dist/`, `build/` | Tidak ada, dan merupakan hasil instalasi/build jika ada |
| File/log sementara | Tidak relevan untuk konteks source |

## 5. Status pengujian terakhir

- `python -m unittest discover -s tests -v` → **47 tests OK**
- `python uji_end_to_end.py ...` → seluruh tahap **LULUS**
- Perhitungan tetap identik dengan `cbr.py` sebagai kode acuan.
