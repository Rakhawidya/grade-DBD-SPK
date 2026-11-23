# DOKUMENTASI PROJECT — SPK berbasis Case-Based Reasoning (CBR)

Dokumen ini menjelaskan seluruh project secara runtut agar mampu
**dijelaskan sendiri kepada dosen** tanpa bantuan AI.

---

## 1. Arsitektur Aplikasi

Aplikasi dibagi menjadi 3 lapis dengan tanggung jawab tegas:

```
┌─────────────────────────────────────────────────────────┐
│  ui/          LAPISAN TAMPILAN (Streamlit)              │
│               Menerima input user, menampilkan hasil.  │
│               TIDAK memuat perhitungan.                 │
└───────────────────────┬─────────────────────────────────┘
                        │ memanggil
┌───────────────────────▼─────────────────────────────────┐
│  services/    LAPISAN DATABASE & VALIDASI               │
│               CRUD kriteria, kasus, riwayat;            │
│               validasi form.                            │
│               TIDAK memuat perhitungan CBR.             │
└───────────────────────┬─────────────────────────────────┘
                        │ menyediakan data
┌───────────────────────▼─────────────────────────────────┐
│  core/        LAPISAN PERHITUNGAN INTI (murni Python)   │
│               cosine.py : dot product, panjang vektor,  │
│                           cosine similarity             │
│               cbr.py    : Retrieve, Reuse, Revise,      │
│                           Retain                        │
│               TIDAK mengimpor Streamlit maupun database.│
└─────────────────────────────────────────────────────────┘
```

**Mengapa dipisah?** Agar perhitungan dapat diuji secara terpisah
(`tests/test_perhitungan.py` berjalan tanpa Streamlit dan tanpa database)
dan agar logika matematika tidak tercemar kode tampilan.

---

## 2. Struktur Folder

```
spk-db/
├── app.py                     # Entry point + navigasi sidebar
├── cbr.py                     # Kode acuan dari dosen (tidak diubah)
├── requirements.txt
├── README.md
├── DOKUMENTASI.md             # Dokumen ini
│
├── core/
│   ├── __init__.py
│   ├── cosine.py              # Perhitungan Cosine Similarity manual
│   └── cbr.py                 # 4 tahap CBR
│
├── services/
│   ├── __init__.py
│   ├── database.py            # Koneksi, tabel, data awal
│   ├── kriteria.py            # CRUD kriteria
│   ├── kasus.py               # CRUD kasus
│   ├── riwayat.py             # Simpan/baca riwayat konsultasi
│   └── validasi.py            # Aturan validasi input
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py           # Beranda + tombol mulai pemeriksaan
│   ├── konsultasi.py          # Cek Gejala: input → hasil → tinjau → simpan
│   ├── riwayat.py             # Arsip pemeriksaan + kartu rincian
│   ├── tema.py                # Design system, brand, stepper, gauge, kartu
│   └── helper.py              # Tabel dan format angka (tanpa perhitungan)
│
├── tests/
│   ├── __init__.py
│   ├── test_perhitungan.py    # 24 unit test matematika CBR
│   ├── test_database.py       # 16 test database + validasi + alur lengkap
│   └── test_ui.py             # 10 test integrasi antarmuka (AppTest Streamlit)
│
└── uji_end_to_end.py          # Uji HTTP ke server Streamlit yang berjalan
```

Halaman manajemen kasus dan kriteria sengaja dihilangkan dari aplikasi. Paket
`services/` tetap menyimpan CRUD karena dibutuhkan untuk menyiapkan data awal,
menyimpan hasil, dan menjaga urutan vektor. Prototipe HTML statis lama dan
workflow GitHub Pages yang hanya menyajikan prototipe tersebut sudah dihapus;
styling aktif seluruhnya berada di `ui/tema.py`.

---

## 3. Alur Data dari Input hingga Hasil

```
[1] USER membuka menu "Cek Gejala"
        │
[2] FORM menampilkan data pasien + daftar gejala dari tabel `kriteria`
        │   (urutan diambil dari kolom urutan -> menjamin urutan vektor sama)
        ▼
[3] USER mengcentang gejala lalu menekan "Periksa Sekarang"
        │
[4] services/validasi.py  memeriksa:
        │   - nama kasus terisi
        │   - minimal satu gejala dicentang
        │   - panjang vektor == jumlah kriteria
        ▼
[5] core/cbr.py :: bangun_vektor()
        │   dict {G01:1, G02:0, ...} -> list [1, 0, ..., 0]
        ▼
[6] services/kasus.py :: daftar_kasus()
        │   mengambil SEMUA kasus lama + nilai gejalanya dari SQLite
        ▼
[7] core/cbr.py :: siapkan_kasus_lama()
        │   mengubah tiap kasus lama menjadi list vektor berurutan sama
        ▼
[8] core/cbr.py :: retrieve()  ──► core/cosine.py
        │       dot product + panjang vektor + cosine, semua manual
        ▼
[9] Hasil diurutkan & diberi peringkat  ->  ditampilkan ke USER
        │
[10] core/cbr.py :: reuse()    -> rekomendasi solusi awal
[11] core/cbr.py :: revise()   -> USER meninjau / mengoreksi solusi
[12] core/cbr.py :: retain()   -> payload disiapkan
        │
[13] services/kasus.py + services/riwayat.py
        │   kasus baru + riwayat pemeriksaan + detail perbandingan
        ▼
[14] DATABASE SQLite (spk_dbd.db)
        │
[15] Kasus baru otomatis menjadi PEMBANDING pada pemeriksaan berikutnya
```

---

## 4. Alur Metode CBR

### 4.1 Retrieve (Pencarian)
**Kode:** `core/cbr.py :: retrieve()`

Membandingkan kasus baru dengan **seluruh** kasus lama menggunakan
Cosine Similarity, lalu mengurutkan dari kemiripan tertinggi.

Hasil tiap perbandingan disimpan lengkap:
`dot product`, `panjang vektor baru`, `panjang vektor lama`,
`cosine similarity`, `persentase`, `peringkat`.

### 4.2 Reuse (Pemanfaatan)
**Kode:** `core/cbr.py :: reuse()`

Mengambil solusi dari kasus dengan cosine tertinggi sebagai **rekomendasi awal**.

### 4.3 Revise (Peninjauan)
**Kode:** `core/cbr.py :: revise()` + form di `ui/konsultasi.py`

User meninjau rekomendasi:
- kolom solusi **dikosongkan** → rekomendasi diterima (`sumber = "rekomendasi"`)
- kolom solusi **diisi lain** → koreksi user menjadi final (`sumber = "koreksi user"`)

Ada kolom catatan peninjauan untuk alasan perubahan.

### 4.4 Retain (Penyimpanan)
**Kode:** `core/cbr.py :: retain()` (menyiapkan payload)
→ `services/kasus.py :: tambah_kasus()` + `services/riwayat.py :: simpan_konsultasi()`

Kasus baru + solusi final disimpan ke database, sehingga pada konsultasi
berikutnya jumlah kasus pembanding bertambah. Ini inti pembelajaran CBR:
**sistem makin kaya pengetahuannya seiring dipakai**.

---

## 5. Penjelasan Cosine Similarity

Cosine Similarity mengukur sudut antara dua vektor. Makin kecil sudutnya,
makin mirip dua vektor.

```
                    dot_product(A, B)
Cosine(A, B) = ─────────────────────────
                 panjang(A) × panjang(B)
```

Hasil berada di rentang **-1 sampai 1**. Karena data gejala hanya bernilai 0/1,
hasilnya berada di rentang **0 sampai 1**, sehingga aman dikalikan 100
menjadi persentase kemiripan.

**Implementasi:** `core/cosine.py :: cosine_similarity()`

---

## 6. Penjelasan Dot Product

Dot product = **jumlah dari perkalian elemen seposisi** kedua vektor.

```
A = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]   (kasus baru)
B = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]   (kasus lama)

dot = 1×1 + 1×0 + 0×0 + ... + 0×1 = 2
```

**Implementasi:**

```python
def rincian_dot_product(vektor_a, vektor_b):
    # Menyimpan tiap perkalian, misalnya [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    perkalian = []
    for i in range(len(vektor_a)):
        perkalian.append(vektor_a[i] * vektor_b[i])
    return perkalian


def dot_product(vektor_a, vektor_b):
    jumlah = 0
    for nilai in rincian_dot_product(vektor_a, vektor_b):
        jumlah += nilai
    return jumlah
```

`rincian_dot_product()` tidak mengubah rumus. Ia hanya menyimpan perkalian
per elemen supaya halaman hasil dapat menampilkan langkah
`1×1 + 1×0 + ... = 2`, bukan hanya angka `2`.

**Makna:** berapa banyak gejala yang **sama-sama muncul** pada kedua kasus.

---

## 7. Penjelasan Panjang Vektor

Panjang vektor (norma Euclidean) = **akar kuadrat dari jumlah kuadrat elemen**.

```
B = [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]

jumlah kuadrat = 1² + 0² + ... + 1² = 5
panjang        = 5 ** 0.5 = 2.2361
```

**Implementasi:**

```python
def jumlah_kuadrat(vektor):
    total = 0
    for nilai in vektor:
        total += nilai ** 2
    return total


def panjang_vektor(vektor):
    return jumlah_kuadrat(vektor) ** 0.5
```

**Makna:** "seberapa banyak" gejala dalam satu kasus, dipakai untuk
**menormalkan** perbandingan supaya kasus dengan banyak gejala tidak selalu
diuntungkan.

**Kondisi khusus:** bila semua elemen 0 → panjang 0 → penyebut 0.
`cosine_similarity()` menangani ini dengan mengembalikan `0.0`
(bukan error pembagian dengan nol).

---

## 8. Penentuan Kasus Terdekat

Dua langkah di `core/cbr.py :: retrieve()`:

**a. Mengurutkan (selection sort manual)**
```python
urut = []
sisa = hasil[:]
while len(sisa) > 0:
    indeks_terbesar = 0
    for i in range(1, len(sisa)):
        if sisa[i]["cosine"] > sisa[indeks_terbesar]["cosine"]:
            indeks_terbesar = i
    urut.append(sisa.pop(indeks_terbesar))
```

**b. Memberi peringkat (kasus sama → peringkat sama)**
```python
for i in range(len(urut)):
    peringkat = 1
    for j in range(len(urutan)):
        if urut[j]["cosine"] > urut[i]["cosine"]:
            peringkat += 1
    urut[i]["peringkat"] = peringkat
```

**c. Mengambil pemenang** — `reuse()` memakai perbandingan `>` eksplisit,
identik dengan logika pada kode acuan `cbr.py`.

---

## 9. Fungsi Database

| Tabel | Fungsi |
|---|---|
| `kriteria` | Menyimpan daftar gejala beserta **urutan** — urutan inilah yang menjamin vektor kasus lama & baru selalu sejajar |
| `kasus` | Identitas kasus: nama, solusi, keterangan, waktu |
| `kasus_nilai` | Nilai 0/1 tiap gejala tiap kasus (relasi banyak-ke-banyak) — menambah kriteria tidak perlu mengubah struktur tabel |
| `konsultasi` | Riwayat konsultasi: vektor input (JSON), kasus acuan, solusi rekomendasi, solusi final, sumber, catatan |
| `konsultasi_detail` | Semua angka perbandingan: dot, panjang ×2, cosine, persentase, peringkat — sehingga hasil lama **bisa diaudit ulang** |

**Koneksi** memakai context manager `with koneksi(...)` agar:
perubahan otomatis ter-commit, error otomatis rollback, dan koneksi selalu
ditutup (di Windows file yang terbuka tidak bisa dihapus).

**Migrasi aman:** hapus kriteria yang sudah dipakai kasus **ditolak**
(`services/kriteria.py :: hapus_kriteria`) agar vektor kasus lama tidak
kehilangan arti.

---

## 10. Library yang Digunakan dan Alasannya

| Library | Status | Alasan |
|---|---|---|
| **Streamlit** | ✅ Dipakai | Framework web Python paling sederhana — cukup fungsi Python biasa, tanpa template HTML terpisah, cocok untuk pembelajaran |
| **sqlite3** | ✅ Dipakai | Modul bawaan Python. Database relasional file tunggal, tanpa instal server |
| **json** | ✅ Dipakai | Modul bawaan — menyimpan vektor input pada tabel riwayat |
| **unittest** | ✅ Dipakai | Modul bawaan — pengujian tanpa instal apa pun |
| **pathlib / datetime** | ✅ Dipakai | Modul bawaan — lokasi file & waktu |
| **NumPy** | ❌ Tidak dipakai | Dilarang — `numpy.dot()`, `numpy.linalg.norm()` akan mengambil alih perhitungan |
| **Pandas** | ❌ Tidak dipakai | Dilarang untuk perhitungan (hanya ikut terpasang sebagai dependensi internal Streamlit untuk tampilan) |
| **Scikit-learn** | ❌ Tidak dipakai | Dilarang — `cosine_similarity()`, nearest neighbor akan menggantikan logika sendiri |
| **SciPy** | ❌ Tidak dipakai | Dilarang — `scipy.spatial.distance` |

---

## 11. Bagian yang Merupakan Perhitungan Manual

Semua di bawah ini **100% ditulis sendiri** dengan `for`, `if`, `def`,
operator indeks, dan operasi aritmatika:

| Fungsi | File | Baris logika |
|---|---|---|
| `rincian_dot_product()` | `core/cosine.py` | Perkalian elemen seposisi (disimpan per elemen) |
| `dot_product()` | `core/cosine.py` | Penjumlahan hasil rincian dengan `for` |
| `jumlah_kuadrat()` | `core/cosine.py` | Jumlah kuadrat tiap elemen |
| `panjang_vektor()` | `core/cosine.py` | Akar kuadrat `** 0.5` dari jumlah kuadrat |
| `cosine_similarity()` | `core/cosine.py` | Pembagian dot / (panjang × panjang) + penanganan penyebut 0 |
| `bangun_vektor()` | `core/cbr.py` | Konversi input → list vektor berurutan |
| `siapkan_kasus_lama()` | `core/cbr.py` | Konversi data kasus → vektor berurutan |
| `retrieve()` | `core/cbr.py` | Perbandingan seluruh kasus + selection sort + peringkat |
| `reuse()` | `core/cbr.py` | Pencarian cosine tertinggi dengan perbandingan `>` |
| `revise()` | `core/cbr.py` | Penentuan solusi final |
| `retain()` | `core/cbr.py` | Penyiapan payload penyimpanan |

**Bukti:** jalankan `grep -r "numpy\|pandas\|sklearn\|scipy" --include=*.py .`
→ tidak ada hasil. Hanya fungsi `cosine_similarity` milik sendiri yang muncul.

---

## 12. Cara Menjalankan Project

```bash
# 1. Pastikan Python 3.10+
python --version

# 2. Install dependensi (hanya Streamlit)
pip install -r requirements.txt

# 3. Jalankan aplikasi
streamlit run app.py
```

Browser terbuka di `http://localhost:8501`. Database + data awal dibuat otomatis.

**Menjalankan pengujian (50 tes):**
```bash
python -m unittest discover -s tests -v
```

**Berkas data:** hapus `spk_dbd.db` kapan saja untuk mengulang dari data awal.

---

## 13. Pembuktian Kesesuaian dengan Kode Acuan

Kode acuan `cbr.py` menghasilkan:

```
Panjang K1 : 2.4495          (= sqrt(6))
data 1: dot 2, cosine 0.3651
data 2: dot 3, cosine 0.5000
data 3: dot 4, cosine 0.6172   <- terbesar
data 4: dot 2, cosine 0.3333
Paling mirip dengan : data lama ke-3
```

`tests/test_perhitungan.py` memakai **angka yang sama persis** sebagai acuan
(`test_cosine_sesuai_kode_acuan`, `test_kasus_paling_mirip_sesuai_kode_acuan`),
dan 4 kasus contoh di database sengaja dibuat identik dengan `data_lama`
sehingga hasil aplikasi dapat langsung dibandingkan.

---

## 14. Skenario Pengujian yang Dicakup

| Skenario | Tes |
|---|---|
| Dot product benar | `test_dot_product_acuan` |
| Rincian perkalian per gejala | `test_rincian_dot_product_dan_jumlahnya` |
| Jumlah kuadrat benar | `test_jumlah_kuadrat_sesuai_kode_acuan` |
| Panjang vektor benar | `test_panjang_k1_sesuai_kode_acuan` |
| Cosine sesuai kode acuan | `test_cosine_sesuai_kode_acuan` |
| Vektor semua nol | `test_cosine_vektor_nol_tidak_menyebabkan_error`, `test_semua_vektor_nol` |
| Jumlah atribut berbeda | `test_dot_product_jumlah_attribut_berbeda`, `test_cosine_jumlah_attribut_berbeda` |
| Data kasus tidak lengkap | `test_siapkan_kasus_lama_vektor_sepanjang_kriteria` (yang tak diisi = 0) |
| Tidak ada kasus pembanding | `test_kosong_tanpa_kasus`, `test_konsultasi_tanpa_kasus_pembanding` |
| Nilai kemiripan sama | `test_nilai_cosine_sama_mendapat_peringkat_sama` |
| Kasus paling mirip | `test_kasus_paling_mirip_sesuai_kode_acuan` |
| Penyimpanan data | `test_tambah_kasus_nilai_tersimpan_urut`, `TestCRUDKriteria` |
| Pengambilan data | `test_tabel_dan_data_awal_terisi`, `test_urutan_kode_konsisten` |
| Alur pemeriksaan penuh | `test_konsultasi_penuh_sesuai_kode_acuan`, `test_pemeriksaan_penuh_lewat_ui` |
| Validasi form | `TestValidasi`, `test_form_kosong_menampilkan_error`, `test_gejala_kosong_menampilkan_error` |
| Detail angka ikut tersimpan di hasil retrieve | `test_retrieve_menyertakan_detail_perhitungan` |
| Kode kriteria duplikat ditolak | `test_kode_duplikat_ditolak_validasi`, `test_kode_duplikat_ditolak_service` |
| Identitas dan menu CEKDBD | `test_identitas_dan_menu_cekd_bd` |
| Tombol perpindahan menu | `test_tombol_mulai_memindah_ke_cek_gejala` |
| Semua halaman render | `TestHalamanRender` |

---

## 15. Panduan Menjelaskan Project ke Dosen

**Q: Kenapa pakai Streamlit?**
> Karena tugasnya aplikasi web dinamis berbasis Python. Streamlit memungkinkan
> seluruh aplikasi ditulis dalam Python murni tanpa HTML/JS terpisah, sehingga
> fokus pada logika CBR, bukan pada framework.

**Q: Mana yang hitung sendiri?**
> Seluruh matematika di `core/cosine.py` dan `core/cbr.py` — dot product,
> panjang vektor, cosine, pengurutan, peringkat. Bisa ditunjukkan baris per baris.

**Q: Apa gunanya library lain?**
> Hanya Streamlit (tampilan) dan sqlite3 (database) — keduanya tidak
> menyentuh perhitungan.

**Q: Bagaimana CBR diimplementasikan?**
> Retrieve = `retrieve()`, Reuse = `reuse()`, Revise = `revise()`
> (ditinjau user lewat form), Retain = `retain()` + penyimpanan ke database.
> Keempatnya berjalan berurutan di satu halaman **Cek Gejala**, bukan dipecah
> menjadi beberapa menu. Rincian perhitungannya tetap bisa dibuka.

**Q: Bagaimana membuktikan hasilnya benar?**
> Menjalankan `python -m unittest discover -s tests -v` — 50 tes, termasuk
> perbandingan langsung dengan angka dari kode acuan `cbr.py`.

**Q: Kenapa urutan kriteria penting?**
> Karena vektor hanyalah list angka tanpa label. Urutan diambil dari kolom
> `urutan` pada tabel `kriteria`, sehingga vektor kasus baru dan kasus lama
> selalu sejajar dan dot product bermakna.

---

## 16. Penyempurnaan Antarmuka CEKDBD

Aplikasi sengaja dibuat seperti website pada umumnya, bukan seperti template AI.
Artinya: warna dibatasi, tipografi rapi, ruang kosong cukup, dan setiap layar
punya satu tujuan yang jelas.

| Penyempurnaan | Lokasi | Alasan |
|---|---|---|
| Identitas CEKDBD + tagline "sistem untuk mendeteksi gejala anda" | `app.py`, `ui/tema.py` | Sidebar langsung menjelaskan apa aplikasi ini, tanpa nama generik |
| Tiga menu saja: Beranda, Cek Gejala, Riwayat | `app.py` | Halaman manajemen kasus/kriteria dihilangkan karena tidak diperlukan pengguna |
| Penomoran menu lewat `format_func=tema.label_menu()` | `app.py`, `ui/tema.py` | Navigasi mudah dipindai; nilai radio asli tetap sederhana |
| Warna netral, aksen hijau tunggal, tanpa gradien generik | `ui/tema.py` | Kesan lebih tenang dan dibuat manusiawi |
| Design token di `:root` untuk warna, font, radius, dan bayangan | `ui/tema.py` | Perubahan desain cukup dilakukan di satu tempat |
| Status fokus hijau pada input, textarea, dan tombol | `ui/tema.py` | Navigasi keyboard terlihat jelas tanpa mengubah identitas visual |
| Dukungan `prefers-reduced-motion` | `ui/tema.py` | Pengguna yang mengurangi animasi tetap mendapat tampilan yang sama |
| Responsivitas lanjutan: kolom dibagi dua di tablet, tombol penuh di ponsel | `ui/tema.py` | Form dan hasil tetap enak dipakai di layar kecil |
| Judul kartu serif memakai `tema.judul_kartu()` | `ui/tema.py`, `ui/dashboard.py`, `ui/konsultasi.py`, `ui/riwayat.py` | Nama kasus dan solusi akhir konsisten di semua halaman |
| Tombol utama menonjol + petunjuk pada field nama | `ui/konsultasi.py` | Aksi utama dan cara mengisi data lebih mudah dipahami |
| Judul dengan *eyebrow*, deskripsi satu paragraf, dan nomor bagian | `tema.header()`, `tema.bagian()` | Hirarki informasi jelas tanpa dekorasi berlebih |
| Langkah Data → Gejala → Analisis → Hasil | `tema.langkah_cbr()` | Pengguna tahu posisinya dalam alur pemeriksaan |
| Hero editorial + tiga langkah singkat di Beranda | `ui/dashboard.py`, `tema.quick_steps()` | Arah masuk jelas tanpa banner besar yang berisik |
| Baris ringkasan label → nilai | `tema.meta_rows()` | Data hasil lebih mudah dipindai daripada paragraf |
| Gejala terpilih ditampilkan sebagai label kecil | `tema.pil_ringkas()` | Pengguna bisa mengonfirmasi input sebelum membaca hasil |
| Catatan bahwa hasil bukan diagnosis medis final | `tema.catatan()`, `ui/konsultasi.py` | Menjaga ekspektasi dan nada aplikasi tetap manusiawi |
| Alur dua langkah: data lalu gejala, dengan tombol **Lanjut** dan **Kembali** | `ui/konsultasi.py` | Satu pertanyaan utama per layar, pengguna tidak perlu mengisi semuanya sekaligus |
| Form gejala dua kolom di dalam kartu langkah 2 | `ui/konsultasi.py` | Mudah dibaca, tetap rapi di layar sempit |
| Tombol **Ubah Gejala** dan **Pemeriksaan Baru** di akhir hasil | `ui/konsultasi.py` | Input bisa dikoreksi atau diulang tanpa kehilangan riwayat |
| Indikator kemiripan berbentuk cincin (*gauge*) | `tema.gauge()` | Persentase kemiripan langsung terbaca di hasil dan riwayat |
| Kartu ringkas pada ringkasan halaman | `tema.kartu_ringkas()`, `ui/riwayat.py` | Angka penting terlihat sebelum membaca tabel |
| Tombol "Mulai Pemeriksaan" di Beranda | `ui/dashboard.py` | Jalan masuk utama jelas tanpa harus mencari menu |
| Rincian dot product, panjang vektor, dan cosine | `ui/konsultasi.py`, `ui/helper.py` | Angka tidak muncul "tiba-tiba"; asalnya bisa diaudit |
| Expander per pemeriksaan di Riwayat | `ui/riwayat.py` | Arsip tetap rapi, tetapi detail lama tetap bisa dibuka |
| Panel tinjau dan simpan dua kolom | `ui/konsultasi.py` | Penjelasan di kiri, aksi di kanan, sehingga keputusan terasa lebih sengaja |
| Daftar peringkat dengan batang kemiripan | `tema.peringkas()` | Tiga kasus terdekat lebih mudah dibandingkan tanpa tabel kaku |
| Aktivitas terbaru berbentuk daftar | `tema.aktivitas_ringkas()` | Riwayat singkat tetap terbaca di layar sempit |
| Pencarian dan ekspor CSV pada Riwayat | `ui/riwayat.py` | Arsip bukan hanya bisa dilihat, tetapi juga dipakai ulang |
| Pesan validasi dan konfirmasi setelah `st.rerun()` | `ui/helper.py`, `ui/konsultasi.py` | Pengguna tidak kehilangan informasi setelah halaman dimuat ulang |
| Data awal otomatis dari `services/database.py` | `services/database.py` | Aplikasi langsung bisa dipakai walaupun menu CRUD tidak ada |

Alur bertahap di atas diselaraskan dengan `files.zip` (berisi
`CEKDBD_Alur_Bertahap.zip` dan `perubahan_alur_bertahap.patch`), lalu dipadukan
dengan penyempurnaan editorial yang sudah ada di proyek. Tombol, stepper, dan
uji antarmuka mengikuti alur **Data → Gejala → Hasil** dari berkas tersebut.

Catatan pengujian antarmuka: karena menu sidebar memakai `format_func`, nilai
yang dikirim Agent API adalah label tampilan seperti `02   Cek Gejala`.
Fungsi `pilihan_menu()` pada `uji_end_to_end.py` mengambil label tersebut dari
tree Streamlit, sehingga uji HTTP tetap benar.

Semua penyempurnaan di atas **tidak mengubah rumus**. Nilai dot product,
panjang vektor, dan cosine tetap sama persis dengan kode acuan `cbr.py`.
