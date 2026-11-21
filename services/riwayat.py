"""
Penyimpanan dan pembacaan riwayat konsultasi.

Tahap RETAIN CBR ditulis di sini: satu konsultasi disimpan bersama
seluruh detail perbandingannya (dot product, panjang vektor, cosine,
peringkat) sehingga hasil lama dapat ditampilkan ulang secara transparan.
"""

import datetime
import json

from services.database import koneksi


def _waktu_sekarang():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def simpan_konsultasi(payload, db_path=None):
    """
    Menyimpan satu riwayat konsultasi + detail perbandingan.

    Parameter `payload` adalah dict berisi:
        nama_kasus_baru, vektor_baru (list), solusi_rekomendasi, solusi_final,
        sumber_solusi, catatan, dan `detail` (daftar hasil retrieve).

    Mengembalikan id konsultasi yang tersimpan.
    """
    with koneksi(db_path) as k:
        kursor = k.execute(
            """
            INSERT INTO konsultasi
                (nama_kasus_baru, vektor_baru, kasus_acuan_id, cosine_tertinggi,
                 solusi_rekomendasi, solusi_final, sumber_solusi, catatan, dibuat_pada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["nama_kasus_baru"],
                json.dumps(payload["vektor_baru"]),
                payload.get("kasus_acuan_id"),
                payload.get("cosine_tertinggi"),
                payload.get("solusi_rekomendasi"),
                payload.get("solusi_final"),
                payload.get("sumber_solusi"),
                payload.get("catatan"),
                _waktu_sekarang(),
            ),
        )
        konsultasi_id = kursor.lastrowid

        for item in payload.get("detail", []):
            k.execute(
                """
                INSERT INTO konsultasi_detail
                    (konsultasi_id, kasus_id, nama_kasus, dot_product,
                     panjang_baru, panjang_lama, cosine, persentase, peringkat)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    konsultasi_id,
                    item.get("kasus_id"),
                    item.get("nama"),
                    item.get("dot_product"),
                    item.get("panjang_baru"),
                    item.get("panjang_lama"),
                    item.get("cosine"),
                    item.get("persentase"),
                    item.get("peringkat"),
                ),
            )

    return konsultasi_id


def daftar_konsultasi(db_path=None):
    """Mengembalikan semua riwayat konsultasi, terbaru di atas."""
    with koneksi(db_path) as k:
        baris = k.execute(
            "SELECT * FROM konsultasi ORDER BY id DESC"
        ).fetchall()
    return [dict(b) for b in baris]


def konsultasi_dengan_id(konsultasi_id, db_path=None):
    """Mengambil satu riwayat konsultasi lengkap dengan vektor inputnya."""
    with koneksi(db_path) as k:
        baris = k.execute(
            "SELECT * FROM konsultasi WHERE id = ?", (konsultasi_id,)
        ).fetchone()
        if baris is None:
            return None
        data = dict(baris)
        data["vektor_baru"] = json.loads(data["vektor_baru"])
        return data


def detail_konsultasi(konsultasi_id, db_path=None):
    """
    Mengambil semua baris perbandingan satu konsultasi,
    urut sesuai peringkat kemiripan.
    """
    with koneksi(db_path) as k:
        baris = k.execute(
            """
            SELECT * FROM konsultasi_detail
            WHERE konsultasi_id = ?
            ORDER BY peringkat, cosine DESC
            """,
            (konsultasi_id,),
        ).fetchall()
    return [dict(b) for b in baris]


def konsultasi_terakhir(db_path=None):
    """Konsultasi paling baru (None bila belum ada), untuk dashboard."""
    with koneksi(db_path) as k:
        baris = k.execute(
            "SELECT * FROM konsultasi ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if baris is None:
            return None
        data = dict(baris)
        data["vektor_baru"] = json.loads(data["vektor_baru"])
        return data


def total_konsultasi(db_path=None):
    with koneksi(db_path) as k:
        return k.execute("SELECT COUNT(*) AS jml FROM konsultasi").fetchone()["jml"]


def total_perbandingan(db_path=None):
    """Total baris perbandingan kasus yang pernah dihitung (untuk dashboard)."""
    with koneksi(db_path) as k:
        return k.execute(
            "SELECT COUNT(*) AS jml FROM konsultasi_detail"
        ).fetchone()["jml"]
