"""
Pengujian database, CRUD, dan alur konsultasi CBR secara menyeluruh.

Dijalankan dengan:
    python -m unittest discover -s tests -v

Setiap tes memakai file database sementara (temp file) sehingga tidak
menyentuh spk_dbd.db yang dipakai aplikasi.
"""

import os
import tempfile
import unittest

from core import cbr
from services import database, kasus, kriteria, riwayat, validasi


class DatabaseTestCase(unittest.TestCase):
    """Kelas dasar: membuat database kosong + 4 kasus acuan tiap tes."""

    def setUp(self):
        # Database sementara yang otomatis terhapus setelah tes selesai
        file_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        file_db.close()
        self.db_path = file_db.name
        database.inisialisasi_database(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


class TestDatabase(DatabaseTestCase):
    def test_env_spk_db_path_dibaca_saat_koneksi(self):
        """SPK_DB_PATH harus dibaca ulang, bukan dibekukan saat import.

        Pengujian UI mengganti environment variable setelah modul database
        di-import. Meng caching DB_PATH akan membuat tes itu menulis ke
        database aplikasi yang nyata.
        """
        f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        f.close()
        lama = os.environ.get("SPK_DB_PATH")
        try:
            os.environ["SPK_DB_PATH"] = f.name
            with database.koneksi() as k:
                baris = k.execute("PRAGMA database_list").fetchone()
            self.assertIsNotNone(baris)
            self.assertEqual(os.path.realpath(baris[2]), os.path.realpath(f.name))
        finally:
            if lama is None:
                os.environ.pop("SPK_DB_PATH", None)
            else:
                os.environ["SPK_DB_PATH"] = lama
            if os.path.exists(f.name):
                os.remove(f.name)

    def test_tabel_dan_data_awal_terisi(self):
        self.assertEqual(len(kriteria.daftar_kriteria(self.db_path)), 14)
        self.assertEqual(len(kasus.daftar_kasus(self.db_path)), 4)
        self.assertEqual(kriteria.total_kriteria(self.db_path), 14)
        self.assertEqual(kasus.total_kasus(self.db_path), 4)

    def test_urutan_kode_konsisten(self):
        urutan = kriteria.urutan_kode(self.db_path)
        self.assertEqual(urutan[0], "G01")
        self.assertEqual(urutan[-1], "G14")
        self.assertEqual(len(urutan), 14)

    def test_inisialisasi_bisa_dijalankan_berulang(self):
        # Idempoten: tidak error dan tidak menduplikasi data
        database.inisialisasi_database(self.db_path)
        self.assertEqual(len(kasus.daftar_kasus(self.db_path)), 4)


class TestCRUDKriteria(DatabaseTestCase):
    def test_tambah_ubah_hapus(self):
        kriteria.tambah_kriteria("G15", "Nyeri Sendi", self.db_path)
        daftar = kriteria.daftar_kriteria(self.db_path)
        self.assertEqual(len(daftar), 15)
        self.assertEqual(daftar[-1]["kode"], "G15")

        target = daftar[-1]
        kriteria.ubah_kriteria(target["id"], "G15", "Nyeri Sendi Berat", self.db_path)
        hasil = [k for k in kriteria.daftar_kriteria(self.db_path)
                 if k["id"] == target["id"]][0]
        self.assertEqual(hasil["nama"], "Nyeri Sendi Berat")

        kriteria.hapus_kriteria(target["id"], self.db_path)
        self.assertEqual(len(kriteria.daftar_kriteria(self.db_path)), 14)

    def test_hapus_kriteria_yang_dipakai_kasus_ditolak(self):
        daftar = kriteria.daftar_kriteria(self.db_path)
        with self.assertRaises(ValueError):
            kriteria.hapus_kriteria(daftar[0]["id"], self.db_path)

    def test_kode_duplikat_ditolak_validasi(self):
        daftar = kriteria.daftar_kriteria(self.db_path)
        pesan = validasi.validasi_kode_kriteria("G01", daftar)
        self.assertIsNotNone(pesan)

    def test_kode_duplikat_ditolak_service(self):
        # Lapisan database tetap menjaga integritas walaupun validasi UI dilewati.
        with self.assertRaises(ValueError):
            kriteria.tambah_kriteria("G01", "Duplikat", self.db_path)

        daftar = kriteria.daftar_kriteria(self.db_path)
        target = daftar[-1]
        with self.assertRaises(ValueError):
            kriteria.ubah_kriteria(target["id"], "G01", "Duplikat", self.db_path)


class TestCRUDKasus(DatabaseTestCase):
    def test_tambah_kasus_nilai_tersimpan_urut(self):
        urutan = kriteria.urutan_kode(self.db_path)
        nilai = {kode: 0 for kode in urutan}
        nilai["G01"] = 1
        nilai["G09"] = 1

        kasus_id = kasus.tambah_kasus(
            "Pasien Uji", "DBD Awal", "tes", nilai, self.db_path
        )

        baru = kasus.kasus_dengan_id(kasus_id, self.db_path)
        self.assertEqual(baru["nama"], "Pasien Uji")
        self.assertEqual(baru["nilai"]["G01"], 1)
        self.assertEqual(baru["nilai"]["G09"], 1)
        self.assertEqual(baru["nilai"]["G02"], 0)
        self.assertEqual(len(baru["nilai"]), 14)

    def test_ubah_kasus(self):
        urutan = kriteria.urutan_kode(self.db_path)
        nilai = {kode: 0 for kode in urutan}
        nilai["G02"] = 1

        kasus_id = kasus.tambah_kasus("Lama", "Solusi Lama", "", nilai, self.db_path)
        kasus.ubah_kasus(kasus_id, "Baru", "Solusi Baru", "ket", nilai, self.db_path)

        hasil = kasus.kasus_dengan_id(kasus_id, self.db_path)
        self.assertEqual(hasil["nama"], "Baru")
        self.assertEqual(hasil["solusi"], "Solusi Baru")

    def test_hapus_kasus(self):
        urutan = kriteria.urutan_kode(self.db_path)
        nilai = {kode: 0 for kode in urutan}
        kasus_id = kasus.tambah_kasus("Hapus Saya", "X", "", nilai, self.db_path)

        kasus.hapus_kasus(kasus_id, self.db_path)
        self.assertIsNone(kasus.kasus_dengan_id(kasus_id, self.db_path))
        self.assertEqual(kasus.total_kasus(self.db_path), 4)


class TestAlurKonsultasiLengkap(DatabaseTestCase):
    """Menguji Retrieve -> Reuse -> Revise -> Retain dari ujung ke ujung."""

    def _vektor_k1(self):
        # Vektor K1 dari kode acuan, dipetakan ke urutan G01..G14
        urutan = kriteria.urutan_kode(self.db_path)
        nilai = {}
        k1 = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        for i in range(len(urutan)):
            nilai[urutan[i]] = k1[i]
        return nilai

    def test_konsultasi_penuh_sesuai_kode_acuan(self):
        nilai = self._vektor_k1()
        urutan = kriteria.urutan_kode(self.db_path)

        # --- Retrieve -----------------------------------------------------
        vektor_baru = cbr.bangun_vektor(nilai, urutan)
        daftar = kasus.daftar_kasus(self.db_path)
        kasus_lama = cbr.siapkan_kasus_lama(daftar, urutan)
        hasil = cbr.retrieve(vektor_baru, kasus_lama)

        # Hasil identik dengan keluaran cbr.py (kode acuan)
        # data 1: 0.3651, data 2: 0.5000, data 3: 0.6172, data 4: 0.3333
        self.assertAlmostEqual(hasil[0]["cosine"], 4 / (6 ** 0.5 * 7 ** 0.5),
                               places=10)
        self.assertAlmostEqual(hasil[1]["cosine"], 0.5, places=10)
        self.assertAlmostEqual(hasil[2]["cosine"], 2 / (6 ** 0.5 * 5 ** 0.5),
                               places=10)
        self.assertAlmostEqual(hasil[3]["cosine"], 2 / 6, places=10)
        self.assertEqual([h["kasus_id"] for h in hasil], [3, 2, 1, 4])

        # --- Reuse --------------------------------------------------------
        rekomendasi = cbr.reuse(hasil)
        self.assertEqual(rekomendasi["kasus_id"], 3)
        self.assertEqual(rekomendasi["solusi"],
                         "Demam Berdarah Dengue (DBD) - Fase Berat")

        # --- Revise (user menerima rekomendasi) ---------------------------
        hasil_revise = cbr.revise(rekomendasi, "", "")
        self.assertEqual(hasil_revise["sumber"], "rekomendasi")

        # --- Retain: simpan kasus baru + riwayat --------------------------
        payload = cbr.retain(vektor_baru, nilai, "Pasien K1",
                             hasil_revise, rekomendasi)
        kasus.tambah_kasus(payload["nama"], payload["solusi_final"],
                           "acuan kasus 3", payload["nilai"], self.db_path)
        konsultasi_id = riwayat.simpan_konsultasi({
            "nama_kasus_baru": payload["nama"],
            "vektor_baru": payload["vektor"],
            "kasus_acuan_id": payload["kasus_acuan_id"],
            "cosine_tertinggi": payload["cosine"],
            "solusi_rekomendasi": rekomendasi["solusi"],
            "solusi_final": payload["solusi_final"],
            "sumber_solusi": payload["sumber_solusi"],
            "catatan": payload["catatan"],
            "detail": hasil,
        }, self.db_path)

        # --- Verifikasi penyimpanan ---------------------------------------
        self.assertEqual(kasus.total_kasus(self.db_path), 5)
        self.assertEqual(riwayat.total_konsultasi(self.db_path), 1)
        self.assertEqual(riwayat.total_perbandingan(self.db_path), 4)

        tersimpan = riwayat.konsultasi_dengan_id(konsultasi_id, self.db_path)
        self.assertEqual(tersimpan["vektor_baru"], vektor_baru)
        self.assertAlmostEqual(tersimpan["cosine_tertinggi"],
                               4 / (6 ** 0.5 * 7 ** 0.5), places=10)

        detail = riwayat.detail_konsultasi(konsultasi_id, self.db_path)
        self.assertEqual(len(detail), 4)
        self.assertEqual(detail[0]["peringkat"], 1)
        self.assertEqual(detail[0]["kasus_id"], 3)

        # --- Kasus hasil Retain kini jadi pembanding berikutnya ------------
        daftar_baru = kasus.daftar_kasus(self.db_path)
        self.assertEqual(len(daftar_baru), 5)
        # Vektor kasus lama tidak berubah urutannya setelah Retain
        vektor_lama_baru = cbr.siapkan_kasus_lama(daftar_baru, urutan)[0]["vektor"]
        self.assertEqual(vektor_lama_baru,
                         [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1])

    def test_konsultasi_tanpa_kasus_pembanding(self):
        # Hapus semua kasus -> Retrieve tidak boleh crash
        for k in kasus.daftar_kasus(self.db_path):
            kasus.hapus_kasus(k["id"], self.db_path)

        urutan = kriteria.urutan_kode(self.db_path)
        vektor = cbr.bangun_vektor({"G01": 1}, urutan)
        hasil = cbr.retrieve(vektor, cbr.siapkan_kasus_lama(
            kasus.daftar_kasus(self.db_path), urutan))

        self.assertEqual(hasil, [])
        self.assertIsNone(cbr.reuse(hasil))


class TestValidasi(DatabaseTestCase):
    def test_teks_wajib(self):
        self.assertIsNotNone(validasi.validasi_teks("", "Nama"))
        self.assertIsNone(validasi.validasi_teks("Pasien A", "Nama"))

    def test_gejala_wajib_dipilih(self):
        kriteria_daftar = kriteria.daftar_kriteria(self.db_path)
        nilai_kosong = {k["kode"]: 0 for k in kriteria_daftar}
        self.assertIsNotNone(
            validasi.validasi_gejala_dipilih(nilai_kosong, kriteria_daftar)
        )

        nilai_ada = dict(nilai_kosong)
        nilai_ada["G01"] = 1
        self.assertIsNone(validasi.validasi_gejala_dipilih(nilai_ada, kriteria_daftar))

    def test_vektor_salah_panjang(self):
        self.assertIsNotNone(validasi.validasi_vektor([1, 0], 14))
        self.assertIsNone(validasi.validasi_vektor([0] * 14, 14))


if __name__ == "__main__":
    unittest.main(verbosity=2)
