from core.cosine import (
    dot_product,
    jumlah_kuadrat,
    panjang_vektor,
    rincian_dot_product,
)


def bangun_vektor(nilai_per_kode, urutan_kode):
    vektor = []
    for kode in urutan_kode:
        if kode in nilai_per_kode and nilai_per_kode[kode] == 1:
            vektor.append(1)
        else:
            vektor.append(0)
    return vektor


def siapkan_kasus_lama(daftar_kasus, urutan_kode):
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


def _hitung_perbandingan(vektor_baru, kasus, panjang_baru, jumlah_kuadrat_baru):
    vektor_lama = kasus["vektor"]

    dot = dot_product(vektor_baru, vektor_lama)
    panjang_lama = panjang_vektor(vektor_lama)
    jumlah_kuadrat_lama = jumlah_kuadrat(vektor_lama)

    penyebut = panjang_baru * panjang_lama
    cosine = dot / penyebut if penyebut != 0 else 0.0

    return {
        "kasus_id": kasus["id"],
        "nama": kasus["nama"],
        "solusi": kasus["solusi"],
        "vektor_lama": vektor_lama,
        "dot_product": dot,

        "rincian_dot": rincian_dot_product(vektor_baru, vektor_lama),
        "jumlah_kuadrat_baru": jumlah_kuadrat_baru,
        "jumlah_kuadrat_lama": jumlah_kuadrat_lama,
        "panjang_baru": panjang_baru,
        "panjang_lama": panjang_lama,
        "cosine": cosine,
        "persentase": cosine * 100,
    }


def _urutkan_tertinggi(hasil):
    urut = []
    sisa = hasil[:]           # salinan supaya list asli tidak hilang isinya
    while len(sisa) > 0:
        indeks_terbesar = 0
        for i in range(1, len(sisa)):
            if sisa[i]["cosine"] > sisa[indeks_terbesar]["cosine"]:
                indeks_terbesar = i
        urut.append(sisa.pop(indeks_terbesar))
    return urut


def _beri_peringkat(urut):
    for i in range(len(urut)):
        peringkat = 1
        for j in range(len(urut)):
            if urut[j]["cosine"] > urut[i]["cosine"]:
                peringkat += 1
        urut[i]["peringkat"] = peringkat
    return urut


def retrieve(vektor_baru, kasus_lama):
    panjang_baru = panjang_vektor(vektor_baru)
    jumlah_kuadrat_baru = jumlah_kuadrat(vektor_baru)
    hasil = []
    for kasus in kasus_lama:
        perbandingan = _hitung_perbandingan(
            vektor_baru, kasus, panjang_baru, jumlah_kuadrat_baru
        )
        hasil.append(perbandingan)
    urut = _urutkan_tertinggi(hasil)
    return _beri_peringkat(urut)


def reuse(hasil_retrieve):
    if len(hasil_retrieve) == 0:
        return None

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
