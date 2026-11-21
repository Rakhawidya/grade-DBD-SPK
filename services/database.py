"""
Modul database: koneksi SQLite, pembuatan tabel, dan data awal.

Database SQLite dipilih karena:
    - bawaan Python (modul sqlite3), tidak perlu instal server
    - file tunggal, mudah dihapus/dibuat ulang saat belajar
    - mendukung relasi (kriteria <-> kasus <-> riwayat)

Struktur tabel:

    kriteria          : daftar gejala/atribut (kode, nama, urutan)
    kasus             : kasus lama (nama, solusi, keterangan)
    kasus_nilai       : nilai 0/1 setiap kriteria pada sebuah kasus
    konsultasi        : riwayat konsultasi + vektor input + solusi final
    konsultasi_detail : hasil perbandingan tiap kasus pada satu konsultasi
                        (dot product, panjang, cosine, peringkat)

Urutan kriteria diambil dari kolom `urutan` sehingga vektor kasus lama dan
kasus baru selalu dibangun dengan urutan yang sama.
"""

import os
import sqlite3

from contextlib import contextmanager
from pathlib import Path

# File database diletakkan di folder project supaya mudah ditemukan.
# Bisa dioverride lewat environment variable SPK_DB_PATH (mis. untuk pengujian
# atau deployment), tanpa mengubah kode.
DB_PATH = Path(os.environ.get(
    "SPK_DB_PATH",
    str(Path(__file__).resolve().parent.parent / "spk_dbd.db"),
))


@contextmanager
def koneksi(db_path=None):
    """
    Membuka koneksi ke database, lalu MENUTUPnya setelah selesai.

    Menggunakan context manager (`with koneksi(...) as k:`) penting karena:
      - perubahan otomatis di-commit bila tidak ada error
      - koneksi selalu ditutup, sehingga file .db tidak terkunci
        (di Windows file yang masih terbuka tidak bisa dihapus/dibaca ulang)

    Urutan penentuan file database:
      1. parameter db_path        (untuk pengujian per fungsi)
      2. environment SPK_DB_PATH  (untuk pengujian aplikasi penuh)
      3. file bawaan spk_dbd.db
    """
    if db_path is not None:
        path = Path(db_path)
    else:
        path = Path(os.environ.get("SPK_DB_PATH", str(DB_PATH)))

    k = sqlite3.connect(str(path))
    k.row_factory = sqlite3.Row   # agar hasil query bisa diakses per kolom
    k.execute("PRAGMA foreign_keys = ON")
    try:
        yield k
        k.commit()
    except Exception:
        k.rollback()
        raise
    finally:
        k.close()


def inisialisasi_database(db_path=None):
    """
    Membuat semua tabel bila belum ada, lalu mengisi data awal
    (kriteria dan kasus contoh) bila tabel masih kosong.
    """
    with koneksi(db_path) as k:
        k.executescript("""
            CREATE TABLE IF NOT EXISTS kriteria (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                kode    TEXT NOT NULL UNIQUE,
                nama    TEXT NOT NULL,
                urutan  INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS kasus (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nama        TEXT NOT NULL,
                solusi      TEXT NOT NULL,
                keterangan  TEXT DEFAULT '',
                dibuat_pada TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS kasus_nilai (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                kasus_id    INTEGER NOT NULL,
                kriteria_id INTEGER NOT NULL,
                nilai       INTEGER NOT NULL DEFAULT 0,
                UNIQUE (kasus_id, kriteria_id),
                FOREIGN KEY (kasus_id)    REFERENCES kasus(id) ON DELETE CASCADE,
                FOREIGN KEY (kriteria_id) REFERENCES kriteria(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS konsultasi (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_kasus_baru   TEXT NOT NULL,
                vektor_baru       TEXT NOT NULL,   -- JSON list [0,1,1,...]
                kasus_acuan_id    INTEGER,
                cosine_tertinggi  REAL,
                solusi_rekomendasi TEXT,
                solusi_final      TEXT,
                sumber_solusi     TEXT,
                catatan           TEXT,
                dibuat_pada       TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS konsultasi_detail (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                konsultasi_id  INTEGER NOT NULL,
                kasus_id       INTEGER,
                nama_kasus     TEXT,
                dot_product    REAL,
                panjang_baru   REAL,
                panjang_lama   REAL,
                cosine         REAL,
                persentase     REAL,
                peringkat      INTEGER,
                FOREIGN KEY (konsultasi_id) REFERENCES konsultasi(id) ON DELETE CASCADE
            );
        """)

        jumlah_kriteria = k.execute("SELECT COUNT(*) AS jml FROM kriteria").fetchone()["jml"]
        if jumlah_kriteria == 0:
            _isi_data_awal(k)


def _isi_data_awal(k):
    """
    Mengisi 14 gejala DBD + 4 kasus contoh.

    Empat vektor kasus contoh sengaja dibuat sama persis dengan `data_lama`
    pada file cbr.py (kode acuan), sehingga hasil perhitungan aplikasi dapat
    dibandingkan langsung dengan kode acuan tersebut.
    """
    import datetime

    gejala = [
        ("G01", "Demam tinggi mendadak", 1),
        ("G02", "Sakit kepala", 2),
        ("G03", "Nyeri di belakang mata", 3),
        ("G04", "Nyeri otot dan sendi", 4),
        ("G05", "Mual atau muntah", 5),
        ("G06", "Lemas / lelah", 6),
        ("G07", "Ruam kulit", 7),
        ("G08", "Perdarahan (mimisan/gusi berdarah)", 8),
        ("G09", "Nyeri perut", 9),
        ("G10", "Muntah darah", 10),
        ("G11", "Feses berdarah", 11),
        ("G12", "Hepar membengkak", 12),
        ("G13", "Trombosit menurun", 13),
        ("G14", "Leukosit menurun", 14),
    ]
    for kode, nama, urutan in gejala:
        k.execute(
            "INSERT INTO kriteria (kode, nama, urutan) VALUES (?, ?, ?)",
            (kode, nama, urutan),
        )

    # Kasus contoh = data_lama dari cbr.py (urutan gejala G01..G14)
    kasus_contoh = [
        ("Kasus contoh 1", "Demam Berdarah Dengue (DBD) - Fase Awal",
         "Data latih dari kode acuan cbr.py",
         [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]),
        ("Kasus contoh 2", "Demam Berdarah Dengue (DBD) - Fase Pertengahan",
         "Data latih dari kode acuan cbr.py",
         [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1]),
        ("Kasus contoh 3", "Demam Berdarah Dengue (DBD) - Fase Berat",
         "Data latih dari kode acuan cbr.py",
         [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1]),
        ("Kasus contoh 4", "Demam Dengue - Variasi Gejala Lain",
         "Data latih dari kode acuan cbr.py",
         [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]),
    ]

    daftar_kriteria = k.execute(
        "SELECT id, kode FROM kriteria ORDER BY urutan"
    ).fetchall()
    sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for nama, solusi, keterangan, nilai_list in kasus_contoh:
        kursor = k.execute(
            "INSERT INTO kasus (nama, solusi, keterangan, dibuat_pada) "
            "VALUES (?, ?, ?, ?)",
            (nama, solusi, keterangan, sekarang),
        )
        kasus_id = kursor.lastrowid
        for i in range(len(nilai_list)):
            k.execute(
                "INSERT INTO kasus_nilai (kasus_id, kriteria_id, nilai) "
                "VALUES (?, ?, ?)",
                (kasus_id, daftar_kriteria[i]["id"], nilai_list[i]),
            )
