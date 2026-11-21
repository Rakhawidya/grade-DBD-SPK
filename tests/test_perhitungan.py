"""
Pengujian unit perhitungan inti CBR dan Cosine Similarity.

Dijalankan dengan:
    python -m unittest discover -s tests -v

Pengujian memakai unittest bawaan Python (tanpa library tambahan).
Angka acuan diambil langsung dari cbr.py (kode dasar yang diberikan dosen),
sehingga terbukti hasil aplikasi sama dengan kode acuan.
"""

import math
import unittest

from core import cbr
from core.cosine import (
    cosine_similarity,
    dot_product,
    jumlah_kuadrat,
    panjang_vektor,
    rincian_dot_product,
)


# Data acuan persis seperti pada file cbr.py
DATA_LAMA = [
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
]
K1 = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]


class TestDotProduct(unittest.TestCase):
    def test_dot_product_acuan(self):
        # Dari kode acuan cbr.py: K1 . data_lama = 2, 3, 4, 2
        self.assertEqual(dot_product(K1, DATA_LAMA[0]), 2)
        self.assertEqual(dot_product(K1, DATA_LAMA[1]), 3)
        self.assertEqual(dot_product(K1, DATA_LAMA[2]), 4)
        self.assertEqual(dot_product(K1, DATA_LAMA[3]), 2)

    def test_dot_product_dengan_data_acak(self):
        self.assertEqual(dot_product([1, 2, 3], [4, 5, 6]), 32)
        self.assertEqual(dot_product([0, 0], [1, 1]), 0)

    def test_dot_product_jumlah_attribut_berbeda(self):
        with self.assertRaises(ValueError):
            dot_product([1, 2, 3], [1, 2])

    def test_rincian_dot_product_dan_jumlahnya(self):
        # Rincian dipakai UI untuk menunjukkan perkalian tiap gejala.
        rincian = rincian_dot_product(K1, DATA_LAMA[0])
        self.assertEqual(
            rincian, [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        )

        jumlah = 0
        for nilai in rincian:
            jumlah += nilai
        self.assertEqual(jumlah, dot_product(K1, DATA_LAMA[0]))

        with self.assertRaises(ValueError):
            rincian_dot_product([1, 0], [1])


class TestPanjangVektor(unittest.TestCase):
    def test_panjang_k1_sesuai_kode_acuan(self):
        # K1 punya 6 elemen bernilai 1 -> "Jumlah K1 = 6", panjang = sqrt(6)
        self.assertEqual(panjang_vektor(K1), 6 ** 0.5)

    def test_jumlah_kuadrat_sesuai_kode_acuan(self):
        # "Jumlah K1 = 6", "Jumlah data lama = 5, 6, 7, 6" pada cbr.py
        self.assertEqual(jumlah_kuadrat(K1), 6)
        self.assertEqual([jumlah_kuadrat(d) for d in DATA_LAMA], [5, 6, 7, 6])

    def test_panjang_vektor_nol(self):
        self.assertEqual(panjang_vektor([0, 0, 0]), 0.0)

    def test_panjang_vektor_data_lama(self):
        # Sesuai keluaran cbr.py: jumlah = 5, 6, 7, 6
        self.assertAlmostEqual(panjang_vektor(DATA_LAMA[0]), math.sqrt(5))
        self.assertAlmostEqual(panjang_vektor(DATA_LAMA[1]), math.sqrt(6))
        self.assertAlmostEqual(panjang_vektor(DATA_LAMA[2]), math.sqrt(7))
        self.assertAlmostEqual(panjang_vektor(DATA_LAMA[3]), math.sqrt(6))


class TestCosineSimilarity(unittest.TestCase):
    def test_cosine_sesuai_kode_acuan(self):
        """
        Cosine K1 terhadap keempat data lama, persis seperti keluaran cbr.py:

        panjang K1 = sqrt(6)
        data 1: 2 / (sqrt(6) * sqrt(5)) = 0.3651
        data 2: 3 / (sqrt(6) * sqrt(6)) = 0.5000
        data 3: 4 / (sqrt(6) * sqrt(7)) = 0.6172   <- tertinggi
        data 4: 2 / (sqrt(6) * sqrt(6)) = 0.3333
        """
        panjang_k1 = math.sqrt(6)
        expected = [
            2 / (panjang_k1 * math.sqrt(5)),
            3 / (panjang_k1 * math.sqrt(6)),
            4 / (panjang_k1 * math.sqrt(7)),
            2 / (panjang_k1 * math.sqrt(6)),
        ]
        for i, data in enumerate(DATA_LAMA):
            self.assertAlmostEqual(
                cosine_similarity(K1, data), expected[i], places=10,
                msg=f"cosine ke-{i + 1} tidak sama dengan kode acuan",
            )

    def test_cosine_identik_maksimal(self):
        self.assertAlmostEqual(cosine_similarity([1, 1, 0], [1, 1, 0]), 1.0)

    def test_cosine_vektor_nol_tidak_menyebabkan_error(self):
        # Penyebut 0 ditangani, hasil dianggap 0 (bukan ZeroDivisionError)
        self.assertEqual(cosine_similarity([0, 0, 0], [1, 1, 0]), 0.0)
        self.assertEqual(cosine_similarity([0, 0], [0, 0]), 0.0)

    def test_cosine_jumlah_attribut_berbeda(self):
        with self.assertRaises(ValueError):
            cosine_similarity([1, 0, 1], [1, 0])


class TestRetrieve(unittest.TestCase):
    """Pengujian Retrieve: urutan, peringkat, dan kasus paling mirip."""

    def _kasus_lama(self):
        return [
            {"id": i + 1, "nama": f"Kasus {i + 1}", "solusi": f"Solusi {i + 1}",
             "vektor": data}
            for i, data in enumerate(DATA_LAMA)
        ]

    def test_hasil_terurut_dan_peringkat(self):
        hasil = cbr.retrieve(K1, self._kasus_lama())

        self.assertEqual(len(hasil), 4)

        # Hasil wajib terurut dari cosine tertinggi
        for i in range(len(hasil) - 1):
            self.assertGreaterEqual(hasil[i]["cosine"], hasil[i + 1]["cosine"])

        # Peringkat 1 dimiliki kasus cosine tertinggi
        self.assertEqual(hasil[0]["peringkat"], 1)

    def test_kasus_paling_mirip_sesuai_kode_acuan(self):
        """
        Dari keluaran cbr.py: cosine terbesar = 0.6172 pada data lama ke-3.
        Urutan kemiripan: data 3 (0.6172) > data 2 (0.5) > data 1 (0.3651)
        > data 4 (0.3333).
        """
        hasil = cbr.retrieve(K1, self._kasus_lama())
        rekomendasi = cbr.reuse(hasil)

        self.assertEqual(rekomendasi["kasus_id"], 3)
        self.assertAlmostEqual(rekomendasi["cosine"], 4 / (6 ** 0.5 * 7 ** 0.5),
                               places=10)

        # Urutan penuh sesuai kode acuan
        urutan_id = [h["kasus_id"] for h in hasil]
        self.assertEqual(urutan_id, [3, 2, 1, 4])

    def test_retrieve_menyertakan_detail_perhitungan(self):
        hasil = cbr.retrieve(K1, self._kasus_lama())
        terbaik = hasil[0]

        self.assertEqual(terbaik["jumlah_kuadrat_baru"], 6)
        self.assertEqual(terbaik["jumlah_kuadrat_lama"], 7)
        self.assertEqual(len(terbaik["rincian_dot"]), len(K1))

        jumlah_rincian = 0
        for nilai in terbaik["rincian_dot"]:
            jumlah_rincian += nilai
        self.assertEqual(jumlah_rincian, terbaik["dot_product"])

    def test_nilai_cosine_sama_mendapat_peringkat_sama(self):
        # Dua kasus identik -> cosine sama -> keduanya peringkat 1
        kembar = [
            {"id": 10, "nama": "A", "solusi": "-", "vektor": [1, 1, 0, 0]},
            {"id": 11, "nama": "B", "solusi": "-", "vektor": [1, 1, 0, 0]},
            {"id": 12, "nama": "C", "solusi": "-", "vektor": [0, 0, 1, 1]},
        ]
        hasil = cbr.retrieve([1, 1, 0, 0], kembar)
        peringkat = {h["kasus_id"]: h["peringkat"] for h in hasil}

        self.assertEqual(peringkat[10], 1)
        self.assertEqual(peringkat[11], 1)
        self.assertEqual(peringkat[12], 3)

    def test_kosong_tanpa_kasus(self):
        self.assertEqual(cbr.retrieve(K1, []), [])
        self.assertIsNone(cbr.reuse([]))

    def test_semua_vektor_nol(self):
        kosong = [{"id": 9, "nama": "Nol", "solusi": "-", "vektor": [0, 0, 0]}]
        hasil = cbr.retrieve([0, 0, 0], kosong)
        self.assertEqual(hasil[0]["cosine"], 0.0)
        # cosine 0 tetap boleh jadi "paling mirip" karena satu-satunya pilihan
        self.assertEqual(cbr.reuse(hasil)["kasus_id"], 9)


class TestBangunVektor(unittest.TestCase):
    def urutan(self):
        return ["G01", "G02", "G03"]

    def test_urutan_sesuai_kriteria(self):
        vektor = cbr.bangun_vektor({"G03": 1, "G01": 1}, self.urutan())
        self.assertEqual(vektor, [1, 0, 1])   # G02 tidak dipilih -> 0

    def test_kosong_jadi_nol_semua(self):
        self.assertEqual(cbr.bangun_vektor({}, self.urutan()), [0, 0, 0])

    def test_siapkan_kasus_lama_vektor_sepanjang_kriteria(self):
        kasus = [
            {"id": 1, "nama": "A", "solusi": "X", "nilai": {"G01": 1, "G03": 1}},
            {"id": 2, "nama": "B", "solusi": "Y", "nilai": {"G02": 1}},
        ]
        siap = cbr.siapkan_kasus_lama(kasus, self.urutan())
        self.assertEqual(siap[0]["vektor"], [1, 0, 1])
        self.assertEqual(siap[1]["vektor"], [0, 1, 0])


class TestReviseRetain(unittest.TestCase):
    def test_revise_terima_rekomendasi(self):
        rekomendasi = {"kasus_id": 1, "nama": "A", "solusi": "DBD Awal",
                       "cosine": 0.9, "persentase": 90.0,
                       "dot_product": 5, "panjang_baru": 5, "panjang_lama": 5}
        hasil = cbr.revise(rekomendasi, "", "")
        self.assertEqual(hasil["solusi_final"], "DBD Awal")
        self.assertEqual(hasil["sumber"], "rekomendasi")

    def test_revise_koreksi_user(self):
        rekomendasi = {"kasus_id": 1, "nama": "A", "solusi": "DBD Awal",
                       "cosine": 0.9, "persentase": 90.0,
                       "dot_product": 5, "panjang_baru": 5, "panjang_lama": 5}
        hasil = cbr.revise(rekomendasi, "DBD Berat", "perlu cek trombosit")
        self.assertEqual(hasil["solusi_final"], "DBD Berat")
        self.assertEqual(hasil["sumber"], "koreksi user")
        self.assertEqual(hasil["catatan"], "perlu cek trombosit")

    def test_retain_menyiapkan_payload_lengkap(self):
        rekomendasi = {"kasus_id": 2, "nama": "B", "solusi": "Y",
                       "cosine": 0.8, "persentase": 80.0,
                       "dot_product": 4, "panjang_baru": 5, "panjang_lama": 5}
        hasil_revise = {"solusi_final": "Y baru", "sumber": "koreksi user",
                        "catatan": "catatan"}
        payload = cbr.retain([1, 0, 1], {"G01": 1, "G03": 1}, "Kasus Baru",
                             hasil_revise, rekomendasi)

        self.assertEqual(payload["nama"], "Kasus Baru")
        self.assertEqual(payload["solusi_final"], "Y baru")
        self.assertEqual(payload["vektor"], [1, 0, 1])
        self.assertEqual(payload["kasus_acuan_id"], 2)
        self.assertAlmostEqual(payload["cosine"], 0.8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
