"""
Fungsi bantu tampilan (bukan perhitungan).

Hanya mengubah struktur data hasil retrieve menjadi baris tabel/teks yang
mudah dibaca Streamlit, serta mengelola pesan feedback antar-rerun.
Tidak ada logika matematika di sini: semua angka sudah dihitung di `core/`.
"""

import streamlit as st


def set_flash(pesan, tipe="success"):
    """
    Menyimpan pesan feedback sebentar di session_state.

    Streamlit menjalankan ulang script setelah tombol form ditekan. Pesan
    `st.success()` yang dibuat tepat sebelum `st.rerun()` ikut hilang, jadi
    pesan disimpan dulu dan ditampilkan pada run berikutnya oleh
    `tampilkan_flash()`.
    """
    st.session_state["_spk_flash"] = {"pesan": pesan, "tipe": tipe}


def tampilkan_flash():
    """Menampilkan (lalu menghapus) pesan feedback yang tersimpan."""
    flash = st.session_state.pop("_spk_flash", None)
    if flash is None:
        return

    pesan = flash["pesan"]
    tipe = flash["tipe"]
    if tipe == "error":
        st.error(pesan)
    elif tipe == "warning":
        st.warning(pesan)
    elif tipe == "info":
        st.info(pesan)
    else:
        st.success(pesan)


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


def baris_gejala(nilai):
    """
    Mengubah dict nilai {kode: 0/1} menjadi baris "Kode | Gejala | Nilai"
    sesuai urutan kriteria, untuk menampilkan vektor kasus secara terbuka.
    """
    from services.kriteria import daftar_kriteria

    baris = []
    for kr in daftar_kriteria():
        baris.append({
            "Kode": kr["kode"],
            "Gejala": kr["nama"],
            "Nilai": nilai.get(kr["kode"], 0),
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
