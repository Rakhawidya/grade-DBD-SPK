import datetime
import os
import sqlite3

from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "spk_dbd.db"


def _path_database():
    return Path(os.environ.get("SPK_DB_PATH") or str(DB_PATH))


def waktu_sekarang():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hitung_baris(k, tabel, syarat=None, parameter=()):
    sql = f"SELECT COUNT(*) AS jml FROM {tabel}"
    if syarat:
        sql += f" WHERE {syarat}"
    return k.execute(sql, parameter).fetchone()["jml"]


@contextmanager
def koneksi(db_path=None):
    if db_path is not None:
        path = Path(db_path)
    else:
        path = _path_database()

    k = sqlite3.connect(str(path))
    k.row_factory = sqlite3.Row   # agar hasil query bisa diakses per kolom
    try:
        k.execute("PRAGMA foreign_keys = ON")
        yield k
        k.commit()
    except Exception:
        k.rollback()
        raise
    finally:
        k.close()


def inisialisasi_database(db_path=None):
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

        jumlah_kriteria = hitung_baris(k, "kriteria")
        if jumlah_kriteria == 0:
            _isi_data_awal(k)


def _isi_data_awal(k):
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
        "SELECT id, kode FROM kriteria ORDER BY urutan, id"
    ).fetchall()
    sekarang = waktu_sekarang()

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
