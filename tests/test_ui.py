"""
Pengujian integrasi antarmuka memakai AppTest bawaan Streamlit.

AppTest menjalankan aplikasi Streamlit di dalam proses Python (tanpa browser),
sehingga dapat memastikan setiap halaman render tanpa exception dan
alur konsultasi benar-benar berfungsi dari form sampai Retain.

Dijalankan dengan:
    python -m unittest discover -s tests -v
"""

import os
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from core import cbr
from services import database, kasus, kriteria, riwayat

# Path absolut ke app.py (AppTest menyelesaikan path relatif terhadap file pemanggil)
APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


def jalankan_app(halaman="Dashboard"):
    """Menjalankan app.py dengan menu sidebar tertentu."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    if at.sidebar.radio[0].value != halaman:
        at.sidebar.radio[0].set_value(halaman).run()
    return at


class TestHalamanRender(unittest.TestCase):
    """Setiap halaman wajib ter-render tanpa exception."""

    def test_dashboard_render(self):
        at = jalankan_app("Dashboard")
        self.assertEqual(len(at.exception), 0, at.exception)
        self.assertTrue(len(at.title) > 0)

    def test_halaman_kasus_render(self):
        at = jalankan_app("Manajemen Kasus")
        self.assertEqual(len(at.exception), 0, at.exception)

    def test_halaman_kriteria_render(self):
        at = jalankan_app("Manajemen Kriteria")
        self.assertEqual(len(at.exception), 0, at.exception)

    def test_halaman_riwayat_render(self):
        at = jalankan_app("Riwayat Perhitungan")
        self.assertEqual(len(at.exception), 0, at.exception)

    def test_halaman_konsultasi_render(self):
        at = jalankan_app("Konsultasi Baru")
        self.assertEqual(len(at.exception), 0, at.exception)


class TestAlurKonsultasiDiUI(unittest.TestCase):
    """Menguji alur lengkap Retrieve -> Reuse -> Revise -> Retain lewat UI."""

    def setUp(self):
        # Database sementara supaya tidak mengubah spk_dbd.db
        import tempfile

        f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        f.close()
        self.db_path = f.name
        database.inisialisasi_database(self.db_path)

        # Aplikasi yang dijalankan AppTest membaca environment variable ini
        self._db_path_lama = os.environ.get("SPK_DB_PATH")
        os.environ["SPK_DB_PATH"] = self.db_path

    def tearDown(self):
        if self._db_path_lama is None:
            os.environ.pop("SPK_DB_PATH", None)
        else:
            os.environ["SPK_DB_PATH"] = self._db_path_lama

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_konsultasi_penuh_lewat_ui(self):
        at = jalankan_app("Konsultasi Baru")

        # Isi nama kasus baru
        at.text_input[0].set_value("Pasien Uji UI")
        # Centang G01, G02, G04 (seperti vektor K1 pada kode acuan)
        kunci_dicentang = []
        for cb in at.checkbox:
            label = str(cb.label)
            if label.startswith(("Demam tinggi", "Sakit kepala", "Nyeri otot")):
                cb.set_value(True)
                kunci_dicentang.append(label)

        self.assertEqual(len(kunci_dicentang), 3, "Gejala uji tidak ditemukan")

        # Tekan tombol Proses CBR
        tombol_proses = [
            b for b in at.button if "Proses CBR" in str(b.label)
        ]
        self.assertEqual(len(tombol_proses), 1)
        tombol_proses[0].click().run()

        self.assertEqual(len(at.exception), 0, at.exception)

        # Hasil Retrieve harus tampil (judul tahap)
        judul = [str(s.value) for s in at.subheader]
        self.assertTrue(any("Retrieve" in j for j in judul), judul)
        self.assertTrue(any("Reuse" in j for j in judul), judul)

        # --- Revise: user menerima rekomendasi --------------------------
        tombol_revise = [b for b in at.button if "Validasi Solusi" in str(b.label)]
        self.assertEqual(len(tombol_revise), 1)
        tombol_revise[0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)

        # --- Retain: simpan ke database ---------------------------------
        tombol_retain = [b for b in at.button if "Retain" in str(b.label)]
        self.assertEqual(len(tombol_retain), 1)
        tombol_retain[0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)

        # --- Verifikasi benar-benar tersimpan ----------------------------
        self.assertEqual(kasus.total_kasus(self.db_path), 5)
        self.assertEqual(riwayat.total_konsultasi(self.db_path), 1)
        self.assertEqual(riwayat.total_perbandingan(self.db_path), 4)

        # Kasus baru kini menjadi pembanding
        urutan = kriteria.urutan_kode(self.db_path)
        vektor_baru = cbr.bangun_vektor(
            {"G01": 1, "G02": 1, "G04": 1}, urutan
        )
        hasil = cbr.retrieve(
            vektor_baru,
            cbr.siapkan_kasus_lama(kasus.daftar_kasus(self.db_path), urutan),
        )
        self.assertEqual(len(hasil), 5)

    def test_feedback_tambah_kriteria_muncul_setelah_rerun(self):
        """
        Pesan sukses harus tetap tampil setelah st.rerun().
        Ini menguji mekanisme flash message di ui/helper.py.
        """
        at = jalankan_app("Manajemen Kriteria")

        field_kode = [t for t in at.text_input if str(t.label) == "Kode"][0]
        field_nama = [
            t for t in at.text_input if str(t.label) == "Nama Gejala"
        ][0]
        field_kode.set_value("G15")
        field_nama.set_value("Nyeri Sendi Uji")

        tombol = [
            b for b in at.button if "Simpan Kriteria" in str(b.label)
        ][0]
        tombol.click().run()

        self.assertEqual(len(at.exception), 0, at.exception)
        pesan = [str(s.value) for s in at.success]
        self.assertTrue(
            any("berhasil ditambahkan" in p for p in pesan), pesan
        )
        self.assertEqual(len(kriteria.daftar_kriteria(self.db_path)), 15)

    def test_form_kosong_menampilkan_error(self):
        at = jalankan_app("Konsultasi Baru")

        # Tekan proses tanpa mengisi apa pun
        tombol = [b for b in at.button if "Proses CBR" in str(b.label)][0]
        tombol.click().run()

        self.assertEqual(len(at.exception), 0, at.exception)
        # Harus ada pesan error validasi, bukan crash
        self.assertTrue(len(at.error) > 0, "Tidak ada pesan error validasi")


if __name__ == "__main__":
    unittest.main(verbosity=2)
