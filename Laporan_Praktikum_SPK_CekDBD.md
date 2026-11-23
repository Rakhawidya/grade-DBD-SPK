# LAPORAN PRAKTIKUM SISTEM PENDUKUNG KEPUTUSAN (SPK) – CEKDBD

> Disusun berdasarkan analisis langsung terhadap project CekDBD. File `DHF`, `P006`, dan `cosine_similarity.py` tidak ditemukan; pemetaan ke data aktual dijelaskan di dalam laporan.

## Daftar Isi

- BAB I – PENDAHULUAN
  - 1.1 Latar Belakang
  - 1.2 Tujuan Praktikum
  - 1.3 Ruang Lingkup dan Batasan
- BAB II – ISI
  - 2.1 Dasar Teori
  - 2.2 Alat dan Bahan
  - 2.3 Dataset (DHF dan P006)
  - 2.4 Langkah Kerja
  - 2.5 Implementasi Kode
  - 2.6 Hasil Percobaan
- BAB III – PENUTUP
  - 3.1 Kesimpulan

## BAB I – PENDAHULUAN

### 1.1 Latar Belakang

Sistem Pendukung Keputusan (SPK) adalah sistem informasi yang membantu pengguna mengambil keputusan dengan menyajikan data, pengetahuan, dan prosedur analisis yang terstruktur. Dalam praktikum ini, fokusnya bukan menggantikan keputusan pakar, melainkan menyediakan pendekatan bantu yang dapat dijelaskan langkah demi langkah.

Demam Berdarah Dengue (DBD) memiliki beragam gejala, mulai dari demam tinggi, nyeri di belakang mata, nyeri otot dan sendi, hingga tanda lanjutan seperti perdarahan dan penurunan trombosit. Mengenali pola gejala secara manual memerlukan pengalaman, sehingga sistem berbasis pengetahuan kasus menjadi relevan untuk membantu proses pencocokan.

CekDBD memilih Case-Based Reasoning (CBR) karena sistem menyimpan kasus-kasus sebelumnya dan membandingkan kasus baru dengan kasus lama. Pada tahap pencarian kasus, sistem memakai Cosine Similarity untuk mengukur seberapa mirip dua vektor gejala. Seluruh perhitungan ditulis manual dengan Python dasar agar dapat ditunjukkan baris per baris kepada dosen.

Secara ringkas, CekDBD adalah aplikasi Streamlit dengan tiga halaman, yaitu Beranda, Cek Gejala, dan Riwayat. Sistem memproses 14 gejala biner, membandingkannya dengan kasus pembanding yang tersimpan di SQLite, lalu menampilkan rekomendasi awal beserta rincian dot product, panjang vektor, nilai cosine, persentase kemiripan, dan peringkat.

### 1.2 Tujuan Praktikum

- Memahami konsep SPK dan perannya dalam membantu pengambilan keputusan berbasis pengetahuan.
- Memahami metode Case-Based Reasoning serta empat tahapnya: Retrieve, Reuse, Revise, dan Retain.
- Memahami perhitungan Cosine Similarity dan hubungannya dengan dot product serta panjang vektor.
- Mengimplementasikan metode tersebut pada sistem CekDBD menggunakan Python murni dan SQLite.
- Menguji proses pencocokan kasus dengan data aktual project dan membandingkan hasil manual dengan hasil program.

### 1.3 Ruang Lingkup dan Batasan

Ruang lingkup laporan mengikuti implementasi yang ada: input berupa nama atau kode pasien dan pilihan gejala G01–G14, proses pencocokan memakai CBR dan Cosine Similarity manual, keluaran berupa rekomendasi solusi kasus terdekat beserta rincian perhitungannya.

- Dataset aktual adalah 14 kriteria gejala dan empat kasus contoh yang dibuat oleh services/database.py; vektornya identik dengan data_lama pada cbr.py.
- Setiap gejala bernilai 0 atau 1. Tidak ada kolom bobot pada tabel kriteria maupun kasus_nilai, sehingga bobot tidak dimodelkan secara eksplisit.
- Kategori hasil bukan kolom diagnosis medis, melainkan label solusi pada kasus pembanding, seperti 'DBD - Fase Awal' hingga 'Fase Berat'.
- Hasil sistem berupa rekomendasi awal yang dapat ditinjau dan dikoreksi pengguna; sistem menyatakan secara eksplisit bahwa hasilnya bukan diagnosis medis final.
- File bernama DHF, P006, dan cosine_similarity.py tidak ditemukan di folder project, files.zip, arsip bersarang, maupun riwayat Git. Laporan ini memetakan 'DHF' ke data_lama, 'P006' ke k1, dan 'cosine_similarity.py' ke core/cosine.py dengan catatan eksplisit pada bagian terkait.
- Sumber eksternal dataset tidak tercantum di project, sehingga tidak dapat diverifikasi dan tidak dikarang dalam laporan ini.
- Spesifikasi perangkat keras dan nama editor/IDE tidak tercantum di project, sehingga tidak dinyatakan secara spesifik.

## BAB II – ISI

### 2.1 Dasar Teori

Sistem Pendukung Keputusan menyediakan bantuan analitis bagi pengguna. Dalam CekDBD, bantuan tersebut berupa perbandingan kasus: pengguna memilih gejala, sistem mencari kasus lama yang paling mirip, lalu menyajikan solusi kasus tersebut sebagai rekomendasi awal.

Case-Based Reasoning adalah pendekatan penyelesaian masalah berbasis pengetahuan kasus. Pengalaman sebelumnya disimpan sebagai kasus, dan kasus baru diselesaikan dengan mencari kasus lama yang serupa. Siklusnya terdiri dari empat tahap yang diimplementasikan di core/cbr.py:

- Retrieve: membandingkan kasus baru dengan seluruh kasus lama dan mengurutkan hasil dari kemiripan tertinggi.
- Reuse: mengambil solusi dari kasus paling mirip sebagai rekomendasi awal.
- Revise: pengguna meninjau rekomendasi; kolom solusi kosong berarti rekomendasi diterima, kolom terisi berarti koreksi pengguna menjadi solusi final.
- Retain: kasus baru beserta solusi final disiapkan lalu disimpan melalui layanan database, sehingga menjadi pembanding pada pemeriksaan berikutnya.

CBR dan Cosine Similarity merupakan dua konsep yang berbeda. CBR adalah pendekatan penyelesaian masalah secara keseluruhan, sedangkan Cosine Similarity hanyalah teknik pengukur kemiripan yang dipakai pada tahap Retrieve. Dengan kata lain, cosine tidak menggantikan siklus CBR; ia menjadi komponen matematis di dalam salah satu tahapnya.

Representasi kasus berupa vektor biner berurutan. Jika kriteria berurutan G01 hingga G14, maka vektor memiliki 14 elemen. Gejala yang dicentang bernilai 1 dan yang tidak dicentang bernilai 0. Urutan diambil dari kolom urutan tabel kriteria agar vektor kasus baru dan kasus lama sejajar.

**Rumus:** `cos(A, B) = (A · B) / (‖A‖ × ‖B‖) = Σᵢ₌₁ⁿ(aᵢ × bᵢ) / ( √(Σᵢ₌₁ⁿ aᵢ²) × √(Σᵢ₌₁ⁿ bᵢ²) )`

Simbol A dan B adalah dua vektor gejala yang dibandingkan; aᵢ dan bᵢ adalah nilai elemen ke-i masing-masing vektor; n adalah jumlah kriteria, yaitu 14; A · B adalah dot product atau jumlah perkalian elemen seposisi; ‖A‖ dan ‖B‖ adalah panjang vektor (norma Euclidean). Karena data bernilai 0/1, hasil cosine berada pada rentang 0 sampai 1 dan dikalikan 100 untuk ditampilkan sebagai persentase. Jika salah satu panjang bernilai nol, fungsi mengembalikan 0,0 untuk mencegah pembagian dengan nol.

Hubungan rumus dengan kode: rincian_dot_product() menyimpan perkalian per elemen, dot_product() menjumlahkannya, jumlah_kuadrat() menghitung Σaᵢ², panjang_vektor() mengakar jumlah kuadrat, dan cosine_similarity() menggabungkan semuanya. Pada core/cbr.py, fungsi retrieve() memakai kembali dot dan panjang yang sudah dihitung agar tidak dihitung dua kali, dengan rumus yang sama.

### 2.2 Alat dan Bahan

Alat dan bahan berikut dipilih berdasarkan impor, konfigurasi, dan file yang benar-benar ada di project.

**Tabel 1. Alat dan bahan yang digunakan dalam project CekDBD.**

| No | Alat/Bahan | Peran dalam Project | Bukti di Project |
|---|---|---|---|
| 1 | Python 3.10+ (eksekusi: 3.15.2) | Menjalankan seluruh logika perhitungan dan aplikasi | python --version; file .py pada core/, services/, ui/ |
| 2 | Streamlit ≥ 1.40 (eksekusi: 1.67.0) | Menyusun antarmuka web tiga halaman | requirements.txt; app.py |
| 3 | SQLite melalui modul sqlite3 | Menyimpan kriteria, kasus, dan riwayat dalam spk_dbd.db | services/database.py; spk_dbd.db |
| 4 | Modul bawaan: math, json, datetime, os, pathlib, contextlib, unittest | Pembantu perhitungan, JSON vektor, waktu, path, koneksi, pengujian | Impor pada core/, services/, tests/ |
| 5 | CSS inline melalui st.markdown | Design token, tata letak responsif, tombol, gauge, kartu | ui/tema.py |
| 6 | unittest + Streamlit AppTest | Menguji perhitungan, database, alur UI | tests/test_perhitungan.py; tests/test_database.py; tests/test_ui.py |
| 7 | Sistem operasi Windows (platform terdeteksi win32) | Lingkungan eksekusi pengujian | Informasi lingkungan terminal |
| 8 | Editor/IDE | Tidak dapat dipastikan | Tidak tercantum di project |
| 9 | Spesifikasi perangkat keras | Tidak dapat dipastikan | Tidak tercantum di project |

Tidak ada NumPy, Pandas, scikit-learn, atau SciPy yang dipakai untuk perhitungan. Dependensi numerik yang mungkin ikut terpasang bersama Streamlit tidak diimpor oleh kode project.

### 2.3 Dataset (DHF dan P006)

Pemeriksaan terhadap folder project, files.zip, arsip CEKDBD_Alur_Bertahap.zip, dan riwayat Git tidak menemukan file bernama DHF maupun P006. Agar laporan tetap dapat dipertanggungjawabkan, penulisan berikut digunakan: yang disebut 'dataset DHF' adalah empat kasus pembanding pada data_lama di cbr.py dan seed services/database.py; yang disebut 'data P006' adalah vektor kasus baru k1 pada cbr.py. Kedua sebutan ini adalah penanda laporan, bukan nama file yang ditemukan.

Dataset DHF memiliki 14 atribut gejala biner. Urutan atribut ditentukan oleh kolom urutan pada tabel kriteria. Tidak ada bobot eksplisit; bobot dapat dipahami sebagai implisit sama, yaitu 1 untuk gejala yang muncul dan 0 untuk gejala yang tidak muncul. Tampilan mengelompokkan G01–G07 sebagai 'Keluhan umum' dan G08–G14 sebagai 'Tanda lanjutan', tetapi pengelompokan ini hanya untuk keterbacaan formulir dan tidak mengubah urutan vektor.

**Tabel 2. Struktur atribut dataset DHF (14 kriteria pada services/database.py).**

| Kode | Nama Gejala | Kelompok Tampilan | Nilai | Bobot |
|---|---|---|---|---|
| G01 | Demam tinggi mendadak | Keluhan umum | 0/1 | Tidak didefinisikan |
| G02 | Sakit kepala | Keluhan umum | 0/1 | Tidak didefinisikan |
| G03 | Nyeri di belakang mata | Keluhan umum | 0/1 | Tidak didefinisikan |
| G04 | Nyeri otot dan sendi | Keluhan umum | 0/1 | Tidak didefinisikan |
| G05 | Mual atau muntah | Keluhan umum | 0/1 | Tidak didefinisikan |
| G06 | Lemas / lelah | Keluhan umum | 0/1 | Tidak didefinisikan |
| G07 | Ruam kulit | Keluhan umum | 0/1 | Tidak didefinisikan |
| G08 | Perdarahan (mimisan/gusi berdarah) | Tanda lanjutan | 0/1 | Tidak didefinisikan |
| G09 | Nyeri perut | Tanda lanjutan | 0/1 | Tidak didefinisikan |
| G10 | Muntah darah | Tanda lanjutan | 0/1 | Tidak didefinisikan |
| G11 | Feses berdarah | Tanda lanjutan | 0/1 | Tidak didefinisikan |
| G12 | Hepar membengkak | Tanda lanjutan | 0/1 | Tidak didefinisikan |
| G13 | Trombosit menurun | Tanda lanjutan | 0/1 | Tidak didefinisikan |
| G14 | Leukosit menurun | Tanda lanjutan | 0/1 | Tidak didefinisikan |

Empat kasus pembanding memiliki label solusi sebagai kategori: Kasus contoh 1 'DBD - Fase Awal', Kasus contoh 2 'DBD - Fase Pertengahan', Kasus contoh 3 'DBD - Fase Berat', dan Kasus contoh 4 'Demam Dengue - Variasi Gejala Lain'. Keterangan tiap kasus menyebut 'Data latih dari kode acuan cbr.py'. Sumber dataset dari luar project tidak tercantum, sehingga tidak dinyatakan.

**Tabel 3. Struktur data P006 yang dipetakan ke vektor k1 pada cbr.py.**

| Aspek | Isi Aktual di Project | Keterangan |
|---|---|---|
| File dataset P006 | Tidak ditemukan | Tidak ada di project, files.zip, arsip bersarang, dan Git |
| Vektor pengganti | [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0] | k1 pada cbr.py baris 8 |
| Jumlah atribut | 14 | Sama dengan jumlah kriteria G01–G14 |
| Gejala bernilai 1 | G01, G02, G04, G08, G09, G10 | Enam gejala dicentang |
| Jumlah kuadrat | 6 | Enam elemen bernilai 1 |
| Panjang vektor | √6 ≈ 2,4495 | Dipakai sebagai penyebut cosine |
| Kategori/solusi | Tidak ditentukan | k1 hanya vektor input; solusi berasal dari kasus pembanding |
| Peran | Kasus baru yang dicocokkan | Menjadi kasus tetap hanya bila hasil disimpan pengguna |

Perbedaan utama keduanya: data DHF adalah kumpulan kasus lama yang sudah memiliki solusi dan berfungsi sebagai pembanding, sedangkan data P006/k1 adalah satu vektor kasus baru tanpa label solusi yang menjadi input perhitungan. Keduanya memakai skema atribut yang sama dan sama-sama tidak memiliki bobot eksplisit.

### 2.4 Langkah Kerja

Alur praktikum mengikuti urutan eksekusi aktual pada aplikasi, mulai dari menyiapkan lingkungan hingga hasil disimpan.

**Tabel 4. Tahapan langkah kerja praktikum CekDBD.**

| No | Tahap | Aktivitas | File/Fungsi Terkait | Keluaran |
|---|---|---|---|---|
| 1 | Persiapan project | Membuat lingkungan Python, memasang Streamlit, menjalankan aplikasi | requirements.txt; app.py | Aplikasi berjalan di localhost:8501 |
| 2 | Pemeriksaan dataset | Membaca kriteria, kasus contoh, dan vektor acuan | cbr.py; services/database.py; spk_dbd.db | 14 gejala, 4 kasus awal, vektor k1 |
| 3 | Pemrosesan input gejala | Mengisi nama/kode pasien dan mencentang gejala | ui/konsultasi.py; services/validasi.py | Dict nilai {G01:0/1, ...} |
| 4 | Pembentukan vektor | Mengubah dict menjadi list berurutan | core/cbr.py :: bangun_vektor() | Vektor baru 14 elemen |
| 5 | Perhitungan cosine | Menghitung dot, jumlah kuadrat, panjang, cosine | core/cosine.py | Nilai kemiripan per kasus |
| 6 | Pencocokan CBR | Menyiapkan kasus lama dan mengurutkan hasil | core/cbr.py :: retrieve() | Daftar peringkat kasus |
| 7 | Penentuan hasil | Mengambil solusi kasus peringkat pertama | core/cbr.py :: reuse() | Rekomendasi awal |
| 8 | Penampilan dan penyimpanan | Menampilkan gauge, rincian, tinjauan; menyimpan hasil | ui/konsultasi.py; services/riwayat.py | Hasil tampil dan tersimpan di database |

Alur kerja sistem CekDBD dapat diuraikan secara berurutan sebagai berikut.

1. Pengguna membuka aplikasi Streamlit dan memilih menu Cek Gejala. Halaman menampilkan formulir identitas pasien serta daftar gejala G01–G14 yang dibagi menjadi keluhan umum (G01–G07) dan tanda lanjutan (G08–G14).
2. Pengguna mengisi nama atau kode pasien, lalu mencentang minimal satu gejala. Modul services/validasi.py memeriksa kewajiban nama, jumlah gejala, dan panjang vektor sebelum proses dilanjutkan.
3. Nilai gejala dalam bentuk {G01: 0/1, …, G14: 0/1} diubah oleh bangun_vektor() pada core/cbr.py menjadi vektor biner berisi 14 elemen. Urutannya mengikuti kolom urutan tabel kriteria, sehingga setiap elemen memiliki makna yang sama pada semua kasus.
4. Sistem membaca kasus pembanding dari spk_dbd.db melalui services/kasus.py. Fungsi siapkan_kasus_lama() mengubah setiap kasus menjadi vektor 14 elemen yang sejajar dengan vektor input.
5. Tahap Retrieve pada core/cbr.py menghitung panjang dan jumlah kuadrat vektor baru satu kali, lalu untuk setiap kasus lama menghitung rincian perkalian, dot product, jumlah kuadrat, panjang vektor, cosine similarity, dan persentase kemiripan.
6. Seluruh hasil diurutkan dari nilai cosine tertinggi ke terendah, kemudian diberi peringkat. Kasus dengan nilai cosine yang sama memperoleh peringkat yang sama sesuai _beri_peringkat() pada core/cbr.py.
7. Tahap Reuse mengambil solusi dari kasus berperingkat pertama sebagai rekomendasi awal. Sebagai ilustrasi, untuk vektor k1 kasus dengan cosine tertinggi adalah Kasus contoh 3 dengan solusi 'DBD - Fase Berat' sebesar 0,6172.
8. Antarmuka menampilkan gauge persentase, ringkasan tiga kasus terdekat, tabel rincian perbandingan, dan kolom tinjauan. Pada tahap Revise, pengguna dapat menerima rekomendasi apa adanya atau menulis koreksi sebagai solusi akhir.
9. Tahap Retain menyiapkan payload kasus baru beserta solusi final, lalu services/riwayat.py menyimpannya ke tabel konsultasi dan konsultasi_detail. Kasus yang tersimpan menjadi data pembanding pada pemeriksaan berikutnya.

Uraian di atas memperlihatkan bahwa perhitungan cosine berada di dalam tahap Retrieve, bukan mencakup seluruh metode CBR. Setelah hasil ditinjau dan disimpan, kasus baru kembali menjadi data pembanding untuk pemeriksaan berikutnya.

### 2.5 Implementasi Kode

Dua file utama yang dianalisis adalah modul perhitungan cosine dan modul logika CBR. File bernama cosine_similarity.py tidak ditemukan; fungsi cosine_similarity() berada di core/cosine.py. File cbr.py yang dimaksud dalam pembahasan implementasi adalah core/cbr.py, sedangkan cbr.py di root project berperan sebagai kode acuan pembanding hasil.

**Tabel 5. Penjelasan fungsi komponen utama kode.**

| File | Fungsi/Objek | Tugas Utama | Hubungan |
|---|---|---|---|
| core/cosine.py | rincian_dot_product() | Menyimpan perkalian tiap pasangan elemen | Bahan penjelasan dot product di UI |
| core/cosine.py | dot_product() | Menjumlahkan perkalian elemen seposisi | Pembilang rumus cosine |
| core/cosine.py | jumlah_kuadrat() | Menjumlahkan kuadrat elemen vektor | Penyusun panjang vektor |
| core/cosine.py | panjang_vektor() | Mengakar jumlah kuadrat | Penyebut rumus cosine |
| core/cosine.py | cosine_similarity() | Menggabungkan dot dan panjang menjadi kemiripan | Dipakai langsung pada pengujian |
| core/cbr.py | bangun_vektor() | Mengubah input dict menjadi vektor berurutan | Menjamin urutan sama dengan kriteria |
| core/cbr.py | siapkan_kasus_lama() | Menyiapkan vektor kasus dari database | Input bagi retrieve() |
| core/cbr.py | retrieve() | Membandingkan semua kasus, mengurut, memberi peringkat | Memanggil fungsi core/cosine.py |
| core/cbr.py | reuse() | Memilih solusi kasus cosine tertinggi | Rekomendasi awal |
| core/cbr.py | revise() | Menentukan solusi final dan sumber solusi | Masukan tahap Retain |
| core/cbr.py | retain() | Menyiapkan payload kasus baru | Ditulis ke database oleh services/ |
| cbr.py (root) | data_lama, k1 | Vektor acuan dan contoh kasus baru | Pembanding hasil implementasi |

**Kode 1. Fungsi cosine_similarity pada core/cosine.py (baris 91–110).**

```python
def cosine_similarity(vektor_a, vektor_b):
    """
    Cosine Similarity = dot_product(a, b) / (panjang(a) * panjang(b)).

    Nilai berada di rentang -1 sampai 1. Untuk data gejala biner (0/1) hasilnya
    berada di rentang 0 sampai 1, sehingga aman dikalikan 100 menjadi persentase.

    Kondisi khusus: jika salah satu vektor bernilai nol semua (panjang = 0),
    penyebut menjadi 0. Pembagian dengan nol dicegah dengan mengembalikan 0.0,
    artinya "tidak ada kemiripan yang bisa diukur".
    """
    dot = dot_product(vektor_a, vektor_b)
    panjang_a = panjang_vektor(vektor_a)
    panjang_b = panjang_vektor(vektor_b)

    penyebut = panjang_a * panjang_b
    if penyebut == 0:
        return 0.0

    return dot / penyebut
```

Fungsi menerima dua list vektor, menghitung dot product dan kedua panjang vektor, lalu membagi dot dengan hasil kali panjang. Pemeriksaan penyebut sama dengan nol mencegah error pada kasus vektor nol. Fungsi ini murni: tidak membaca database juga tidak menampilkan hasil.

**Kode 2. Fungsi retrieve pada core/cbr.py (baris 126–142).**

```python
def retrieve(vektor_baru, kasus_lama):
    """
    TAHAP RETRIEVE: bandingkan kasus baru dengan seluruh kasus lama.

    Mengembalikan daftar hasil urut dari kemiripan tertinggi. Setiap entri
    memuat semua nilai transparan yang ditampilkan ke user:
        rincian perkalian, dot product, jumlah kuadrat, panjang vektor baru,
        panjang vektor lama, cosine similarity, persentase, dan peringkat.
    """
    panjang_baru = panjang_vektor(vektor_baru)
    jumlah_kuadrat_baru = jumlah_kuadrat(vektor_baru)
    hasil = [
        _hitung_perbandingan(vektor_baru, kasus, panjang_baru, jumlah_kuadrat_baru)
        for kasus in kasus_lama
    ]
    urut = _urutkan_tertinggi(hasil)
    return _beri_peringkat(urut)
```

Fungsi retrieve() menghitung panjang dan jumlah kuadrat kasus baru sekali, meminta _hitung_perbandingan() untuk setiap kasus lama, lalu mengurutkan dan memberi peringkat. Di dalam _hitung_perbandingan(), rumus cosine dihitung ulang dari dot dan panjang yang sudah tersedia, bukan dengan memanggil cosine_similarity(), agar nilai antara tidak dihitung dua kali. Root cbr.py menggunakan logika yang sama secara manual dan dipakai sebagai acuan angka.

### 2.6 Hasil Percobaan

Perhitungan di bawah memakai angka yang benar-benar ada di cbr.py dan services/database.py. Pembulatan empat desimal hanya untuk penyajian; program menyimpan nilai floating-point penuh.

#### 2.6.1 Percobaan 1: Dataset DHF (data aktual data_lama)

Kasus yang digunakan adalah empat kasus pembanding pada data_lama. Inputnya adalah k1, yaitu gejala G01, G02, G04, G08, G09, dan G10 bernilai 1; sepuluh gejala lainnya bernilai 0.

- Vektor input A = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0].
- Jumlah kuadrat A = 1+1+1+1+1+1 = 6, sehingga ‖A‖ = √6 ≈ 2,4495.
- Dot product terhadap Kasus 1 = 1×1 + 1×0 + 0×0 + 1×0 + 0×0 + 0×0 + 0×0 + 1×1 + 1×0 + 1×0 + 0×0 + 0×1 + 0×1 + 0×1 = 2.
- Dot product terhadap Kasus 2 = 2 + (1×1 pada G09) = 3; terhadap Kasus 3 = 3 + (1×1 pada G10) = 4; terhadap Kasus 4 = 1×1 (G01) + 1×1 (G10) = 2.
- Substitusi untuk Kasus 3: cos(A, B₃) = 4 / (√6 × √7) = 4 / √42 ≈ 0,6172, atau 61,72 persen.

**Tabel 6. Hasil perhitungan manual dataset DHF dengan input k1.**

| Kasus | Vektor Pembanding | Dot | ‖B‖ | Substitusi | Manual | Program | Peringkat |
|---|---|---|---|---|---|---|---|
| 1 – Fase Awal | [1,0,0,0,0,0,0,1,0,0,0,1,1,1] | 2 | √5 ≈ 2,2361 | 2/(2,4495×2,2361) | 0,3651 | 0,365148 | 3 |
| 2 – Fase Pertengahan | [1,0,0,0,0,0,0,1,1,0,0,1,1,1] | 3 | √6 ≈ 2,4495 | 3/(2,4495×2,4495) | 0,5000 | 0,500000 | 2 |
| 3 – Fase Berat | [1,0,0,0,0,0,0,1,1,1,0,1,1,1] | 4 | √7 ≈ 2,6458 | 4/(2,4495×2,6458) | 0,6172 | 0,617213 | 1 |
| 4 – Variasi Lain | [1,0,0,0,0,1,0,0,0,1,0,1,1,1] | 2 | √6 ≈ 2,4495 | 2/(2,4495×2,4495) | 0,3333 | 0,333333 | 4 |

Interpretasinya, kasus pembanding dengan kemiripan tertinggi adalah Kasus contoh 3 dengan solusi 'DBD - Fase Berat' dan persentase 61,72 persen. Nilai ini menunjukkan kedekatan pola gejala terhadap kasus tersebut, bukan penegakan diagnosis medis.

#### 2.6.2 Percobaan 2: Dataset P006 (data aktual k1)

Karena file P006 tidak tersedia, percobaan ini memakai k1 sebagaimana telah ditetapkan pada bagian 2.3. Langkah perhitungannya identik dengan percobaan 1, tetapi ringkasan berikut difokuskan pada pembentukan vektor dan kasus pemenang.

**Tabel 7. Hasil perhitungan manual dataset P006 (vektor k1) terhadap kasus pembanding.**

| Komponen | Cara Hitung | Hasil |
|---|---|---|
| Vektor input | G01, G02, G04, G08, G09, G10 = 1; lainnya 0 | [1,1,0,1,0,0,0,1,1,1,0,0,0,0] |
| ‖A‖² | 1²+1²+1²+1²+1²+1² | 6 |
| ‖A‖ | √6 | ≈ 2,4495 |
| Dot terhadap Kasus 3 | 1×1+1×0+0×0+1×0+0×0+0×0+0×0+1×1+1×1+1×1+0×0+0×1+0×1+0×1 | 4 |
| ‖B₃‖² | 1+1+1+1+1+1+1 | 7 |
| ‖B₃‖ | √7 | ≈ 2,6458 |
| Substitusi | 4 / (√6 × √7) = 4 / √42 | ≈ 0,6172 |
| Persentase | 0,6172 × 100 | ≈ 61,72 % |
| Hasil program | cosine_similarity(k1, data_lama[2]) | 0,6172133998 |
| Peringkat program | retrieve() + reuse() | Kasus 3, rekomendasi 'Fase Berat' |

Perbandingan manual dengan program menunjukkan kesesuaian. Nilai manual dibulatkan menjadi 0,3651; 0,5000; 0,6172; dan 0,3333, sedangkan hasil program masing-masing 0,365148; 0,500000; 0,617213; dan 0,333333. Selisih hanya terletak pada digit setelah pembulatan tampilan. Perbedaan tersebut berasal  dari pembulatan di ui/helper.py dan ui/konsultasi.py, bukan dari rumus: ui/helper.py membulatkan empat desimal untuk tabel dan dua desimal untuk persentase, sementara penentuan pemenang memakai nilai asli.

Validasi tambahan dilakukan dengan menjalankan 50 pengujian pada tests/, termasuk perbandingan langsung dengan angka cbr.py dan alur lengkap melalui AppTest. Seluruh pengujian berstatus OK.

## BAB III – PENUTUP

### 3.1 Kesimpulan

- CekDBD diimplementasikan sebagai SPK berbasis pengetahuan kasus dengan tiga halaman Streamlit dan penyimpanan SQLite.
- Siklus CBR terpenuhi melalui Retrieve, Reuse, Revise, dan Retain; Cosine Similarity berperan sebagai ukuran kemiripan pada tahap Retrieve.
- Dataset aktual terdiri dari 14 gejala biner G01–G14 dan empat kasus contoh dengan solusi berupa kategori fase DBD; tidak ada bobot eksplisit dan sumber eksternal tidak tercantum.
- Perhitungan manual dengan input k1 menghasilkan cosine 0,3651; 0,5000; 0,6172; dan 0,3333, dengan Kasus contoh 3 sebagai yang paling mirip.
- Hasil program identik dengan perhitungan manual hingga batas pembulatan tampilan, dan 50 pengujian yang dijalankan berstatus OK.
- File DHF, P006, dan cosine_similarity.py tidak ditemukan di project; laporan ini telah menandai keterbatasan tersebut dan menggunakan data aktual yang dapat diverifikasi sebagai pengganti.
