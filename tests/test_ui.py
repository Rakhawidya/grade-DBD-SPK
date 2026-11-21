"""
Pengujian integrasi antarmuka memakai AppTest bawaan Streamlit.

AppTest menjalankan app.py di dalam proses Python, sehingga setiap halaman
dan alur pemeriksaan dapat diuji tanpa browser.
"""

import os
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from core import cbr
from services import database, kasus, kriteria, riwayat

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


def jalankan_app(halaman="Beranda"):
    """Menjalankan app.py dengan menu sidebar tertentu."""
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    if at.sidebar.radio[0].value != halaman:
        at.sidebar.radio[0].set_value(halaman).run()
    return at


class TestHalamanRender(unittest.TestCase):
    """Setiap halaman wajib ter-render tanpa exception."""

    def test_beranda_render(self):
        at = jalankan_app("Beranda")
        self.assertEqual(len(at.exception), 0, at.exception)
        self.assertTrue(len(at.title) > 0)

    def test_halaman_cek_gejala_render(self):
        at = jalankan_app("Cek Gejala")
        self.assertEqual(len(at.exception), 0, at.exception)

    def test_halaman_riwayat_render(self):
        at = jalankan_app("Riwayat")
        self.assertEqual(len(at.exception), 0, at.exception)

    def test_identitas_dan_menu_cekd_bd(self):
        at = jalankan_app("Beranda")
        teks_sidebar = " ".join(str(m.value) for m in at.sidebar.markdown)
        self.assertIn("CEKDBD", teks_sidebar)
        self.assertIn("sistem untuk mendeteksi gejala anda", teks_sidebar)

        opsi = [str(o) for o in at.sidebar.radio[0].options]
        self.assertEqual(opsi, ["01   Beranda", "02   Cek Gejala", "03   Riwayat"])

    def test_tombol_mulai_memindah_ke_cek_gejala(self):
        at = jalankan_app("Beranda")
        tombol = [b for b in at.button if "Mulai Pemeriksaan" in str(b.label)][0]
        tombol.click().run()
        self.assertEqual(len(at.exception), 0, at.exception)
        self.assertEqual(at.sidebar.radio[0].value, "Cek Gejala")


class TestAlurPemeriksaanDiUI(unittest.TestCase):
    """Menguji alur lengkap dari form sampai penyimpanan hasil."""

    def setUp(self):
        import tempfile

        f = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        f.close()
        self.db_path = f.name
        database.inisialisasi_database(self.db_path)

        self._db_path_lama = os.environ.get("SPK_DB_PATH")
        os.environ["SPK_DB_PATH"] = self.db_path

    def tearDown(self):
        if self._db_path_lama is None:
            os.environ.pop("SPK_DB_PATH", None)
        else:
            os.environ["SPK_DB_PATH"] = self._db_path_lama

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_pemeriksaan_penuh_lewat_ui(self):
        at = jalankan_app("Cek Gejala")

        at.text_input[0].set_value("Pasien Uji UI")
        tombol_lanjut = [b for b in at.button if "Lanjut" in str(b.label)]
        self.assertEqual(len(tombol_lanjut), 1)
        tombol_lanjut[0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)

        dicentang = []
        for cb in at.checkbox:
            label = str(cb.label)
            if label.startswith(("Demam tinggi", "Sakit kepala", "Nyeri otot")):
                cb.set_value(True)
                dicentang.append(label)
        self.assertEqual(len(dicentang), 3, "Gejala uji tidak ditemukan")

        tombol_proses = [b for b in at.button if "Periksa Sekarang" in str(b.label)]
        self.assertEqual(len(tombol_proses), 1)
        tombol_proses[0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)

        judul = [str(s.value) for s in at.subheader]
        self.assertTrue(any("Hasil Pemeriksaan" in j for j in judul), judul)
        self.assertTrue(any("Tinjau Rekomendasi" in j for j in judul), judul)

        tombol_revise = [b for b in at.button if "Simpan Koreksi" in str(b.label)]
        self.assertEqual(len(tombol_revise), 1)
        tombol_revise[0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)
        pesan = [str(s.value) for s in at.success]
        self.assertTrue(
            any("Rekomendasi diterima" in p or "Koreksi tersimpan" in p for p in pesan),
            pesan,
        )

        tombol_retain = [
            b for b in at.button if "Simpan Hasil Pemeriksaan" in str(b.label)
        ]
        self.assertEqual(len(tombol_retain), 1)
        tombol_retain[0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)
        pesan = [str(s.value) for s in at.success]
        self.assertTrue(any("tersimpan" in p.lower() for p in pesan), pesan)

        self.assertEqual(kasus.total_kasus(self.db_path), 5)
        self.assertEqual(riwayat.total_konsultasi(self.db_path), 1)
        self.assertEqual(riwayat.total_perbandingan(self.db_path), 4)

        urutan = kriteria.urutan_kode(self.db_path)
        vektor_baru = cbr.bangun_vektor({"G01": 1, "G02": 1, "G04": 1}, urutan)
        hasil = cbr.retrieve(
            vektor_baru,
            cbr.siapkan_kasus_lama(kasus.daftar_kasus(self.db_path), urutan),
        )
        self.assertEqual(len(hasil), 5)

    def test_form_kosong_menampilkan_error(self):
        at = jalankan_app("Cek Gejala")
        tombol = [b for b in at.button if "Lanjut" in str(b.label)][0]
        tombol.click().run()
        self.assertEqual(len(at.exception), 0, at.exception)
        self.assertTrue(len(at.error) > 0, "Tidak ada pesan error validasi")

    def test_gejala_kosong_menampilkan_error(self):
        at = jalankan_app("Cek Gejala")
        at.text_input[0].set_value("Pasien Tanpa Gejala")
        [b for b in at.button if "Lanjut" in str(b.label)][0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)

        [b for b in at.button if "Periksa Sekarang" in str(b.label)][0].click().run()
        self.assertEqual(len(at.exception), 0, at.exception)
        pesan = [str(e.value) for e in at.error]
        self.assertTrue(any("Pilih minimal satu gejala" in p for p in pesan), pesan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
