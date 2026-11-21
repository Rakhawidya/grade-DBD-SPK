"""
Uji end-to-end aplikasi lewat HTTP ke server Streamlit yang berjalan.

Berbeda dari tests/test_ui.py (in-process), skrip ini membuktikan aplikasi
yang SESUNGUHNYA berjalan di port berfungsi penuh dari form sampai Retain.

Cara pakai:
    1. jalankan server dengan Agent API aktif:
       streamlit run app.py --server.port 8599 --server.enableAgentApi true
    2. python uji_end_to_end.py db_uji.db [nomor_port]

Tanpa `--server.enableAgentApi true`, endpoint /_stcore/agent/interact
menjawab 403 dan pengujian ini tidak bisa dijalankan.

Argumen pertama adalah path database (untuk verifikasi & cleanup). Argumen
kedua opsional berguna bila port 8599 sedang dipakai aplikasi lain.
"""

import json
import os
import sqlite3
import sys
import urllib.request

BASE = "http://localhost:8599"
SESSION = {"id": None}
DB_PATH = None


def panggil(body):
    """Kirim satu permintaan interact dan kembalikan responsnya."""
    if SESSION["id"]:
        body = dict(body)
        body["session_id"] = SESSION["id"]

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        BASE + "/_stcore/agent/interact",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        hasil = json.loads(resp.read().decode("utf-8"))

    if "session_id" in hasil:
        SESSION["id"] = hasil["session_id"]
    return hasil


def semua_elemen(pohon, jenis=None, hasil=None):
    """Menelusuri pohon elemen Streamlit, mengumpulkan node bertipe `jenis`."""
    if hasil is None:
        hasil = []
    if isinstance(pohon, dict):
        if jenis is None or pohon.get("type") == jenis:
            hasil.append(pohon)
        for anak in pohon.get("children", []) or []:
            semua_elemen(anak, jenis, hasil)
    elif isinstance(pohon, list):
        for item in pohon:
            semua_elemen(item, jenis, hasil)
    return hasil


def cari_aksi(respons, kata):
    """Mencari action (trigger) yang labelnya mengandung kata tertentu."""
    for aksi in respons.get("actions", []):
        if kata.lower() in (aksi.get("label") or "").lower():
            return aksi["key"]
    return None


def nilai_widget(respons, tipe, kata_label):
    """Mencari key widget bertipe tertentu dengan label mengandung kata."""
    for aksi in respons.get("actions", []):
        if aksi.get("type") == tipe and kata_label.lower() in (
            aksi.get("label") or ""
        ).lower():
            return aksi["key"]
    return None


def cari_node(pohon, key):
    """Menelusuri tree Streamlit untuk mencari node widget berdasarkan key."""
    if isinstance(pohon, dict):
        if pohon.get("key") == key:
            return pohon
        for anak in pohon.get("children", []) or []:
            hasil = cari_node(anak, key)
            if hasil is not None:
                return hasil
    elif isinstance(pohon, list):
        for item in pohon:
            hasil = cari_node(item, key)
            if hasil is not None:
                return hasil
    return None


def pilihan_menu(respons, key_radio, kata):
    """
    Mengambil nilai radio yang benar untuk dikirim ke Agent API.

    Saat menu memakai `format_func` untuk penomoran, nilai widget yang diterima
    Agent API adalah teks tampilan (mis. "02   Cek Gejala"), bukan nilai aslinya
    ("Cek Gejala").
    """
    node = cari_node(respons.get("tree"), key_radio)
    if node is None:
        return kata

    options = node.get("props", {}).get("options", [])
    for opsi in options:
        if kata.lower() in str(opsi).lower():
            return opsi
    return kata


def cek(nama, kondisi, detail=""):
    if kondisi:
        print(f"  [LULUS] {nama}")
    else:
        print(f"  [GAGAL] {nama} {detail}")
        raise AssertionError(f"{nama}: {detail}")


def bersihkan_data_uji():
    """Menghapus kasus & konsultasi uji agar database kembali bersih."""
    if not DB_PATH or not os.path.exists(DB_PATH):
        return
    with sqlite3.connect(DB_PATH) as k:
        k.execute("PRAGMA foreign_keys = ON")
        k.execute(
            "DELETE FROM kasus WHERE nama = ?", ("Pasien E2E",)
        )
        k.execute(
            "DELETE FROM konsultasi WHERE nama_kasus_baru = ?",
            ("Pasien E2E",),
        )
        k.commit()


def main():
    if len(sys.argv) < 2:
        print("Pakai: python uji_end_to_end.py <path_database> [nomor_port]")
        sys.exit(2)

    global DB_PATH, BASE
    DB_PATH = sys.argv[1]
    if len(sys.argv) >= 3:
        BASE = f"http://localhost:{sys.argv[2]}"
    print(f"Server: {BASE} | database: {DB_PATH}")

    try:
        print("\n=== 1. MUAT APLIKASI ===")
        r = panggil({})
        cek("Aplikasi termuat tanpa error", "tree" in r, str(r)[:300])
        judul = json.dumps(r["tree"])
        cek("Beranda menampilkan ringkasan", "Pemeriksaan tercatat" in judul)
        cek("Menu manajemen tidak ada", "Manajemen Kasus" not in judul)

        print("\n=== 2. BUKA HALAMAN CEK GEJALA ===")
        key_radio = nilai_widget(r, "radio", "Navigasi")
        cek("Menu navigasi ditemukan", key_radio is not None)
        menu_cek = pilihan_menu(r, key_radio, "Cek Gejala")
        r = panggil({"widget_state": {key_radio: menu_cek}})
        cek("Halaman cek gejala terbuka", "Cek Gejala" in json.dumps(r["tree"]))

        print("\n=== 3. ISI FORM: NAMA + GEJALA ===")
        key_nama = nilai_widget(r, "text_input", "Nama atau kode pasien")
        cek("Field nama kasus ditemukan", key_nama is not None)

        # Alur kini bertahap. Langkah 1: nama lalu "Lanjut".
        key_lanjut = cari_aksi(r, "Lanjut")
        cek("Tombol Lanjut ditemukan", key_lanjut is not None)
        r = panggil({"widget_state": {key_nama: "Pasien E2E"}, "trigger": {"key": key_lanjut}})
        cek("Langkah gejala terbuka", "Gejala apa yang Anda rasakan" in json.dumps(r["tree"]))

        # Langkah 2: centang gejala lalu "Periksa Sekarang" (satu request).
        widget_state = {}
        dicentang = []
        for aksi in r.get("actions", []):
            label = (aksi.get("label") or "").lower()
            if aksi.get("type") == "checkbox" and label.startswith(
                ("demam tinggi", "sakit kepala", "nyeri otot")
            ):
                widget_state[aksi["key"]] = True
                dicentang.append(aksi["label"])
        cek("3 gejala ditemukan & dicentang (langkah 2)", len(dicentang) == 3, str(dicentang))
        key_proses = cari_aksi(r, "Periksa Sekarang")
        r = panggil({"widget_state": widget_state, "trigger": {"key": key_proses}})

        isi = json.dumps(r["tree"])
        cek("Hasil pemeriksaan ditampilkan", "Hasil Pemeriksaan" in isi)
        cek("Tinjauan rekomendasi ditampilkan", "Tinjau Rekomendasi" in isi)
        cek("Penyimpanan hasil ditampilkan", "Simpan Hasil" in isi)
        cek("Vektor kasus baru tampil", "vektor gejala anda" in isi.lower())
        cek(
            "Tabel perbandingan tampil",
            "Dot Product" in isi and "Cosine Similarity" in isi,
        )
        cek("Detail langkah perhitungan tampil", "langkah perhitungan" in isi.lower())

        print("\n=== 4. TAHAP TINJAU ===")
        key_revise = cari_aksi(r, "Simpan Koreksi")
        cek("Tombol tinjau ditemukan", key_revise is not None)
        r = panggil({"trigger": {"key": key_revise}})
        isi = json.dumps(r["tree"])
        cek(
            "Solusi final ditetapkan",
            "Rekomendasi diterima" in isi or "Koreksi tersimpan" in isi,
        )

        print("\n=== 5. TAHAP SIMPAN ===")
        key_retain = cari_aksi(r, "Simpan Hasil Pemeriksaan")
        cek("Tombol simpan ditemukan", key_retain is not None)
        r = panggil({"trigger": {"key": key_retain}})
        isi = json.dumps(r["tree"])
        cek("Hasil pemeriksaan tersimpan", "Hasil pemeriksaan tersimpan" in isi)

        print("\n=== 6. VERIFIKASI BERANDA ===")
        key_radio = nilai_widget(r, "radio", "Navigasi")
        r = panggil({"widget_state": {key_radio: pilihan_menu(r, key_radio, "Beranda")}})
        isi = json.dumps(r["tree"])
        cek("Jumlah kasus menjadi 5", '"value":5' in isi.replace(" ", ""), isi[:400])
        cek("Hasil terakhir tampil", "Hasil Terakhir" in isi)
        cek("Vektor input tersimpan", "vektor" in isi.lower())

        print("\n=== 7. VERIFIKASI RIWAYAT ===")
        key_radio = nilai_widget(r, "radio", "Navigasi")
        menu_riwayat = pilihan_menu(r, key_radio, "Riwayat")
        r = panggil({"widget_state": {key_radio: menu_riwayat}})
        isi = json.dumps(r["tree"])
        cek("Riwayat berisi pemeriksaan", "Pasien E2E" in isi)
        cek("Detail perbandingan riwayat tampil", "Dot Product" in isi)

        print("\nSEMUA TAHAP END-TO-END LULUS")
    finally:
        bersihkan_data_uji()
        print("Data uji dibersihkan.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nGAGAL: {exc}", file=sys.stderr)
        sys.exit(1)
