"""
CRUD data kriteria (gejala/atribut).

Kriteria menentukan panjang dan urutan vektor kasus. Karena itu penghapusan
kriteria yang sudah dipakai kasus dicegah, agar vektor kasus lama tidak
tiba-tiba berubah arti.
"""

from services.database import hitung_baris, koneksi


def daftar_kriteria(db_path=None):
    """Mengembalikan semua kriteria urut sesuai kolom `urutan`."""
    with koneksi(db_path) as k:
        baris = k.execute("SELECT * FROM kriteria ORDER BY urutan, id").fetchall()
    return [dict(b) for b in baris]


def urutan_kode(db_path=None):
    """
    Mengembalikan list kode kriteria berurutan, contoh: ["G01", "G02", ...].
    Daftar ini dipakai core/cbr.py untuk menjamin urutan vektor selalu sama.
    """
    return [k["kode"] for k in daftar_kriteria(db_path)]


def tambah_kriteria(kode, nama, db_path=None):
    """Menambah satu kriteria baru. Urutan diletakkan paling akhir."""
    kode = kode.strip().upper()
    nama = nama.strip()

    with koneksi(db_path) as k:
        sama = k.execute(
            "SELECT id FROM kriteria WHERE kode = ?", (kode,)
        ).fetchone()
        if sama is not None:
            raise ValueError(f"Kode kriteria '{kode}' sudah dipakai.")

        jumlah = hitung_baris(k, "kriteria")
        k.execute(
            "INSERT INTO kriteria (kode, nama, urutan) VALUES (?, ?, ?)",
            (kode, nama, jumlah + 1),
        )


def ubah_kriteria(kriteria_id, kode, nama, db_path=None):
    """Mengubah kode dan nama kriteria (tidak mengubah urutan vektor kasus)."""
    kode = kode.strip().upper()
    nama = nama.strip()

    with koneksi(db_path) as k:
        sama = k.execute(
            "SELECT id FROM kriteria WHERE kode = ? AND id != ?",
            (kode, kriteria_id),
        ).fetchone()
        if sama is not None:
            raise ValueError(f"Kode kriteria '{kode}' sudah dipakai.")

        k.execute(
            "UPDATE kriteria SET kode = ?, nama = ? WHERE id = ?",
            (kode, nama, kriteria_id),
        )


def hapus_kriteria(kriteria_id, db_path=None):
    """
    Menghapus kriteria. Ditolak bila sudah dipakai oleh kasus mana pun,
    karena nilai kasus ikut terhapus dan perbandingan menjadi tidak valid.
    """
    with koneksi(db_path) as k:
        dipakai = hitung_baris(
            k, "kasus_nilai", "kriteria_id = ?", (kriteria_id,)
        )

        if dipakai > 0:
            raise ValueError(
                "Kriteria tidak bisa dihapus karena sudah dipakai "
                f"oleh {dipakai} data kasus."
            )

        k.execute("DELETE FROM kriteria WHERE id = ?", (kriteria_id,))


def total_kriteria(db_path=None):
    with koneksi(db_path) as k:
        return hitung_baris(k, "kriteria")
