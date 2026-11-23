"""
CRUD data kasus (kasus lama) beserta nilai gejalanya.

Struktur penyimpanan:
    tabel `kasus`       -> identitas + solusi kasus
    tabel `kasus_nilai` -> satu baris per (kasus, kriteria) bernilai 0/1

Dengan begitu, menambah kriteria baru di masa depan tidak mengubah
struktur tabel kasus.
"""

from services.database import hitung_baris, koneksi, waktu_sekarang
from services.kriteria import daftar_kriteria


def _baca_nilai(k, kasus_id):
    """
    Mengambil nilai kasus berupa dict {kode_kriteria: 0/1}.
    Kriteria yang belum punya baris dianggap 0 (gejala tidak muncul).
    """
    baris = k.execute(
        """
        SELECT k.kode AS kode, kn.nilai AS nilai
        FROM kriteria k
        LEFT JOIN kasus_nilai kn
               ON kn.kriteria_id = k.id AND kn.kasus_id = ?
        ORDER BY k.urutan, k.id
        """,
        (kasus_id,),
    ).fetchall()

    hasil = {}
    for b in baris:
        hasil[b["kode"]] = 0 if b["nilai"] is None else b["nilai"]
    return hasil


def daftar_kasus(db_path=None):
    """
    Mengembalikan semua kasus, masing-masing berisi:
    id, nama, solusi, keterangan, dibuat_pada, dan dict `nilai`.
    """
    with koneksi(db_path) as k:
        baris = k.execute("SELECT * FROM kasus ORDER BY id").fetchall()
        hasil = []
        for b in baris:
            data = dict(b)
            data["nilai"] = _baca_nilai(k, b["id"])
            hasil.append(data)
    return hasil


def kasus_dengan_id(kasus_id, db_path=None):
    """Mengambil satu kasus berdasarkan id (None bila tidak ada)."""
    with koneksi(db_path) as k:
        baris = k.execute("SELECT * FROM kasus WHERE id = ?", (kasus_id,)).fetchone()
        if baris is None:
            return None
        data = dict(baris)
        data["nilai"] = _baca_nilai(k, kasus_id)
        return data


def tambah_kasus(nama, solusi, keterangan, nilai, db_path=None):
    """
    Menyimpan kasus baru + seluruh nilai gejalanya (dict kode -> 0/1).
    Dipakai pada tahap RETAIN CBR maupun form tambah kasus biasa.
    """
    nama = nama.strip()
    solusi = solusi.strip()
    keterangan = (keterangan or "").strip()

    with koneksi(db_path) as k:
        kursor = k.execute(
            "INSERT INTO kasus (nama, solusi, keterangan, dibuat_pada) "
            "VALUES (?, ?, ?, ?)",
            (nama, solusi, keterangan, waktu_sekarang()),
        )
        kasus_id = kursor.lastrowid

        kriteria = daftar_kriteria(db_path)
        for kr in kriteria:
            isi_nilai = nilai.get(kr["kode"], 0)
            k.execute(
                "INSERT INTO kasus_nilai (kasus_id, kriteria_id, nilai) "
                "VALUES (?, ?, ?)",
                (kasus_id, kr["id"], 1 if isi_nilai == 1 else 0),
            )

    return kasus_id


def ubah_kasus(kasus_id, nama, solusi, keterangan, nilai, db_path=None):
    """Mengubah identitas, solusi, dan seluruh nilai gejala kasus."""
    with koneksi(db_path) as k:
        k.execute(
            "UPDATE kasus SET nama = ?, solusi = ?, keterangan = ? WHERE id = ?",
            (nama.strip(), solusi.strip(), (keterangan or "").strip(), kasus_id),
        )

        # Perbarui nilai yang sudah ada, tambahkan yang belum ada.
        kriteria = daftar_kriteria(db_path)
        for kr in kriteria:
            ada = k.execute(
                "SELECT id FROM kasus_nilai WHERE kasus_id = ? AND kriteria_id = ?",
                (kasus_id, kr["id"]),
            ).fetchone()

            isi_nilai = 1 if nilai.get(kr["kode"], 0) == 1 else 0
            if ada is None:
                k.execute(
                    "INSERT INTO kasus_nilai (kasus_id, kriteria_id, nilai) "
                    "VALUES (?, ?, ?)",
                    (kasus_id, kr["id"], isi_nilai),
                )
            else:
                k.execute(
                    "UPDATE kasus_nilai SET nilai = ? "
                    "WHERE kasus_id = ? AND kriteria_id = ?",
                    (isi_nilai, kasus_id, kr["id"]),
                )


def hapus_kasus(kasus_id, db_path=None):
    """Menghapus kasus beserta nilai gejalanya (nilai ikut terhapus via cascade)."""
    with koneksi(db_path) as k:
        k.execute("DELETE FROM kasus WHERE id = ?", (kasus_id,))


def total_kasus(db_path=None):
    with koneksi(db_path) as k:
        return hitung_baris(k, "kasus")
