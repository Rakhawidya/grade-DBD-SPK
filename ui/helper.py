"""
Fungsi bantu tampilan (bukan perhitungan).

Hanya mengubah struktur data hasil retrieve menjadi baris tabel/teks yang
mudah dibaca Streamlit. Tidak ada logika matematika di sini: semua angka
sudah dihitung di `core/`.
"""

def baris_tabel_perbandingan(hasil):
    """
    Mengubah daftar hasil retrieve menjadi daftar dict untuk st.dataframe.
    Angka dibulatkan 4 desimal agar tabel rapi (pembulatan tampilan saja,
    nilai asli tetap dipakai untuk menentukan pemenang).
    """
    baris = []
    for h in hasil:
        baris.append({
            "Peringkat": h["peringkat"],
            "ID Kasus": h["kasus_id"],
            "Nama Kasus": h["nama"],
            "Dot Product": round(h["dot_product"], 4),
            "Panjang Vektor Baru": round(h["panjang_baru"], 4),
            "Panjang Vektor Lama": round(h["panjang_lama"], 4),
            "Cosine Similarity": round(h["cosine"], 4),
            "Kemiripan (%)": round(h["persentase"], 2),
        })
    return baris


def format_vektor(vektor):
    """Contoh output: '[1, 0, 1, 0]' untuk ditampilkan sebagai teks."""
    return "[" + ", ".join(str(v) for v in vektor) + "]"


def format_rincian_dot(vektor_a, vektor_b, rincian, total):
    """
    Menyusun teks langkah dot product, misalnya:

        1×1 + 1×0 + 0×0 + ... = 2

    `rincian` dan `total` berasal dari core/cosine.py. Fungsi ini hanya
    merangkai teks; tidak melakukan perkalian atau penjumlahan sendiri.
    """
    bagian = []
    for i in range(len(rincian)):
        bagian.append(f"{vektor_a[i]}×{vektor_b[i]}")
    return " + ".join(bagian) + f" = {total}"
