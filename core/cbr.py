"""
Logika inti metode Case-Based Reasoning (CBR).

Empat tahapan CBR dipetakan sebagai berikut:

    1. Retrieve -> fungsi retrieve()
       Mencari kasus lama paling mirip dengan kasus baru memakai Cosine
       Similarity (dihitung manual di core/cosine.py).

    2. Reuse    -> fungsi reuse()
       Mengambil solusi dari kasus paling mirip sebagai rekomendasi awal.

    3. Revise   -> fungsi revise()
       Meninjau rekomendasi: diterima apa adanya atau diganti oleh user,
       lalu menghasilkan solusi final.

    4. Retain   -> fungsi retain()
       Menyimpan kasus baru + solusi final. Modul ini hanya menyiapkan
       "payload" penyimpanan; proses menulis ke database dilakukan oleh
       services/ (lihat dokumentasi). Dengan begitu perhitungan tidak
       bercampur dengan akses database.

Seluruh fungsi bersifat murni (tidak membaca database, tidak menampilkan UI)
agar mudah diuji di tests/.
"""

from core.cosine import (
    cosine_similarity,
    dot_product,
    jumlah_kuadrat,
    panjang_vektor,
    rincian_dot_product,
)


def bangun_vektor(nilai_per_kode, urutan_kode):
    """
    Mengubah input user (dict kode -> nilai) menjadi vektor list berurutan.

    Urutan elemen vektor WAJIB sama dengan urutan kriteria pada kasus lama.
    Kriteria yang tidak diisi user dianggap 0 (gejala tidak muncul).
    """
    vektor = []
    for kode in urutan_kode:
        if kode in nilai_per_kode and nilai_per_kode[kode] == 1:
            vektor.append(1)
        else:
            vektor.append(0)
    return vektor


def siapkan_kasus_lama(daftar_kasus, urutan_kode):
    """
    Mengubah data kasus dari database menjadi daftar dict siap hitung:
    [{"id": 1, "nama": "...", "solusi": "...", "vektor": [0,1,1,...]}, ...]

    Nilai kasus lama juga dibangun lewat bangun_vektor() sehingga urutannya
    dijamin sama dengan vektor kasus baru.
    """
    kasus_siap = []
    for kasus in daftar_kasus:
        vektor = bangun_vektor(kasus["nilai"], urutan_kode)
        kasus_siap.append({
            "id": kasus["id"],
            "nama": kasus["nama"],
            "solusi": kasus["solusi"],
            "vektor": vektor,
        })
    return kasus_siap


def retrieve(vektor_baru, kasus_lama):
    """
    TAHAP RETRIEVE: bandingkan kasus baru dengan seluruh kasus lama.

    Mengembalikan daftar hasil urut dari kemiripan tertinggi. Setiap entri
    memuat semua nilai transparan yang ditampilkan ke user:
        rincian perkalian, dot product, jumlah kuadrat, panjang vektor baru,
        panjang vektor lama, cosine similarity, persentase, dan peringkat.
    """
    hasil = []
    panjang_baru = panjang_vektor(vektor_baru)
    jumlah_kuadrat_baru = jumlah_kuadrat(vektor_baru)

    for kasus in kasus_lama:
        vektor_lama = kasus["vektor"]

        dot = dot_product(vektor_baru, vektor_lama)
        panjang_lama = panjang_vektor(vektor_lama)
        jumlah_kuadrat_lama = jumlah_kuadrat(vektor_lama)

        # Cosine dihitung manual; penyebut 0 ditangani oleh cosine_similarity()
        cosine = cosine_similarity(vektor_baru, vektor_lama)

        hasil.append({
            "kasus_id": kasus["id"],
            "nama": kasus["nama"],
            "solusi": kasus["solusi"],
            "vektor_lama": vektor_lama,
            "dot_product": dot,
            # Rincian perkalian dipakai UI untuk menunjukkan asal dot product.
            "rincian_dot": rincian_dot_product(vektor_baru, vektor_lama),
            "jumlah_kuadrat_baru": jumlah_kuadrat_baru,
            "jumlah_kuadrat_lama": jumlah_kuadrat_lama,
            "panjang_baru": panjang_baru,
            "panjang_lama": panjang_lama,
            "cosine": cosine,
            "persentase": cosine * 100,
        })

    # --- Urutkan manual (selection sort sederhana) dari cosine tertinggi ---
    urut = []
    sisa = hasil[:]           # salinan supaya list asli tidak hilang isinya
    while len(sisa) > 0:
        indeks_terbesar = 0
        for i in range(1, len(sisa)):
            if sisa[i]["cosine"] > sisa[indeks_terbesar]["cosine"]:
                indeks_terbesar = i
        urut.append(sisa.pop(indeks_terbesar))

    # --- Beri peringkat; kasus dengan cosine sama mendapat peringkat sama ---
    for i in range(len(urut)):
        peringkat = 1
        for j in range(len(urut)):
            if urut[j]["cosine"] > urut[i]["cosine"]:
                peringkat += 1
        urut[i]["peringkat"] = peringkat

    return urut


def reuse(hasil_retrieve):
    """
    TAHAP REUSE: ambil solusi kasus paling mirip sebagai rekomendasi awal.

    Mengembalikan None bila tidak ada kasus pembanding sama sekali.
    """
    if len(hasil_retrieve) == 0:
        return None

    # hasil sudah urut tertinggi, tetapi pencarian tetap memakai perbandingan
    # eksplisit agar jelas saat dijelaskan (dan aman bila urutan berubah).
    terbaik = hasil_retrieve[0]
    for item in hasil_retrieve:
        if item["cosine"] > terbaik["cosine"]:
            terbaik = item

    return {
        "kasus_id": terbaik["kasus_id"],
        "nama": terbaik["nama"],
        "solusi": terbaik["solusi"],
        "cosine": terbaik["cosine"],
        "persentase": terbaik["persentase"],
        "dot_product": terbaik["dot_product"],
        "panjang_baru": terbaik["panjang_baru"],
        "panjang_lama": terbaik["panjang_lama"],
    }


def revise(rekomendasi, solusi_user, catatan_user=""):
    """
    TAHAP REVISE: tinjau rekomendasi sebelum solusi final ditetapkan.

    - solusi_user kosong  -> rekomendasi diterima apa adanya.
    - solusi_user diisi   -> user mengoreksi, itu menjadi solusi final.

    Mengembalikan dict: solusi_final, sumber ("rekomendasi" / "koreksi user"),
    dan catatan peninjauan.
    """
    solusi_user_bersih = (solusi_user or "").strip()

    if solusi_user_bersih == "" or solusi_user_bersih == rekomendasi["solusi"]:
        solusi_final = rekomendasi["solusi"]
        sumber = "rekomendasi"
    else:
        solusi_final = solusi_user_bersih
        sumber = "koreksi user"

    return {
        "solusi_final": solusi_final,
        "sumber": sumber,
        "catatan": (catatan_user or "").strip(),
    }


def retain(vektor_baru, nilai_per_kode, nama_kasus, hasil_revise, rekomendasi):
    """
    TAHAP RETAIN: siapkan data kasus baru yang akan disimpan ke database.

    Fungsi ini tidak menulis ke database sendiri. Ia hanya membentuk "payload"
    berisi kasus baru + solusi final, supaya logika CBR tetap terpisah dari
    logika penyimpanan (dihandle oleh services/kasus.py dan services/riwayat.py).
    """
    return {
        "nama": nama_kasus,
        "nilai": dict(nilai_per_kode),
        "vektor": list(vektor_baru),
        "solusi_final": hasil_revise["solusi_final"],
        "sumber_solusi": hasil_revise["sumber"],
        "catatan": hasil_revise["catatan"],
        "kasus_acuan_id": rekomendasi["kasus_id"],
        "kasus_acuan_nama": rekomendasi["nama"],
        "cosine": rekomendasi["cosine"],
        "persentase": rekomendasi["persentase"],
    }
