"""
Perhitungan manual Cosine Similarity menggunakan logika Python dasar.

Modul ini sengaja hanya memakai:
    - variabel
    - list
    - for
    - if / else
    - def
    - operasi aritmatika (+, *, **, /)
    - operator indeks []
    - operator pembanding (==, !=, >, <)

TIDAK ada NumPy, Pandas, Scikit-learn, atau SciPy.
Semua fungsi di sini murni (tidak mengubah data input, tidak membaca database,
tidak menampilkan apa pun) supaya mudah diuji dan dijelaskan ke dosen.
"""


def _pastikan_panjang_sama(vektor_a, vektor_b):
    """
    Menjaga urutan dan panjang vektor tetap konsisten.

    Fungsi kecil ini dipakai bersama oleh dot product dan rinciannya supaya
    aturan validasinya tidak ditulis dua kali. Kasus baru dan kasus lama wajib
    dibangun dari daftar kriteria yang sama.
    """
    if len(vektor_a) != len(vektor_b):
        raise ValueError(
            "Jumlah atribut tidak sama: "
            f"{len(vektor_a)} vs {len(vektor_b)}. "
            "Vektor kasus baru dan kasus lama harus sepanjang kriteria yang sama."
        )


def rincian_dot_product(vektor_a, vektor_b):
    """
    Mengembalikan list perkalian per elemen, misalnya [1, 0, 0, 2].

    Dot product adalah penjumlahan dari list ini. Fungsi ini sengaja dipisah
    supaya antarmuka dapat menampilkan langkah perkalian tiap gejala, bukan
    hanya angka akhirnya.
    """
    _pastikan_panjang_sama(vektor_a, vektor_b)

    hasil = []
    for i in range(len(vektor_a)):
        hasil.append(vektor_a[i] * vektor_b[i])
    return hasil


def dot_product(vektor_a, vektor_b):
    """
    Dot product = jumlah dari (vektor_a[i] * vektor_b[i]) untuk setiap i.

    Syarat: jumlah elemen kedua vektor harus sama, karena kasus baru dan kasus
    lama harus dibangun dari urutan kriteria yang sama.
    """
    perkalian = rincian_dot_product(vektor_a, vektor_b)

    jumlah = 0
    for nilai in perkalian:
        jumlah += nilai
    return jumlah


def jumlah_kuadrat(vektor):
    """
    Menjumlahkan kuadrat setiap elemen vektor.

    Ini adalah angka yang sama dengan "Jumlah K1" / "Jumlah data lama" pada
    kode acuan. Dipisah menjadi fungsi sendiri agar bisa ditampilkan di halaman
    hasil sebelum akar kuadrat dihitung.
    """
    total = 0
    for nilai in vektor:
        total += nilai ** 2
    return total


def panjang_vektor(vektor):
    """
    Panjang vektor (norma Euclidean) = akar kuadrat dari jumlah kuadrat elemen.

    Contoh: vektor [1, 1, 0, 1] -> 1^2 + 1^2 + 0^2 + 1^2 = 3 -> 3 ** 0.5
    Dipakai sebagai penyebut pada rumus Cosine Similarity.
    """
    return jumlah_kuadrat(vektor) ** 0.5


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
