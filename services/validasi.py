"""
Validasi input formulir.

Semua fungsi mengembalikan pesan error berbahasa Indonesia (str) bila tidak
valid, atau None bila valid. Pemisahan validasi ke modul sendiri membuat
formulir di UI lebih pendek dan aturan mudah diuji.
"""


def validasi_teks(wajib, nama_field, minimal=3):
    """Memeriksa teks wajib terisi dan panjangnya minimal `minimal` karakter."""
    if wajib is None or str(wajib).strip() == "":
        return f"{nama_field} wajib diisi."
    if len(str(wajib).strip()) < minimal:
        return f"{nama_field} minimal {minimal} karakter."
    return None


def validasi_kode_kriteria(kode, kriteria_sekarang, kriteria_id=None):
    """Memeriksa kode kriteria terisi, formatnya wajib, dan tidak duplikat."""
    if kode is None or kode.strip() == "":
        return "Kode kriteria wajib diisi."

    kode_bersih = kode.strip().upper()
    if " " in kode_bersih:
        return "Kode kriteria tidak boleh mengandung spasi."

    for kr in kriteria_sekarang:
        if kr["kode"].upper() == kode_bersih and kr["id"] != kriteria_id:
            return f"Kode kriteria '{kode_bersih}' sudah dipakai."

    return None


def validasi_gejala_dipilih(nilai, kriteria_sekarang):
    """Kasus/consultasi baru harus punya minimal satu gejala bernilai 1."""
    if len(kriteria_sekarang) == 0:
        return "Belum ada kriteria. Tambahkan kriteria terlebih dahulu."

    for kr in kriteria_sekarang:
        if nilai.get(kr["kode"], 0) == 1:
            return None

    return "Pilih minimal satu gejala."


def validasi_vektor(vektor, jumlah_kriteria):
    """Memastikan panjang vektor cocok dengan jumlah kriteria (pencegah salah urut)."""
    if len(vektor) != jumlah_kriteria:
        return (
            "Panjang vektor tidak cocok dengan jumlah kriteria "
            f"({len(vektor)} vs {jumlah_kriteria})."
        )
    return None
