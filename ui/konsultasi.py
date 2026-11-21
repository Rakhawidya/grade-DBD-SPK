"""
Halaman Cek Gejala: alur lengkap pemeriksaan.

Alur untuk pengguna: isi data → pilih gejala → sistem membandingkan →
lihat rekomendasi → tinjau → simpan. Di belakang layar tetap berjalan empat
tahap CBR: Retrieve, Reuse, Revise, Retain.

Semua angka berasal dari core/cosine.py dan core/cbr.py. File ini hanya
menyiapkan input dan menampilkan hasilnya.
"""

import streamlit as st

from core import cbr
from services import kasus as svc_kasus
from services import kriteria as svc_kriteria
from services import riwayat as svc_riwayat
from services import validasi
from ui import tema
from ui.helper import (
    baris_tabel_perbandingan,
    format_rincian_dot,
    format_vektor,
)


def _kelompokkan_gejala(daftar):
    """
    Membagi gejala menjadi dua kelompok agar daftar panjang lebih mudah dipindai.

    Urutan asli kriteria tidak diubah; fungsi ini hanya menyusun tampilan.
    Nilai tetap disimpan per kode, lalu `cbr.bangun_vektor` yang menentukan
    urutan vektor.
    """
    kelompok = {"awal": [], "lanjutan": []}
    for kr in daftar:
        kode = str(kr.get("kode", ""))
        try:
            nomor = int(kode[1:]) if kode.startswith("G") else 99
        except ValueError:
            nomor = 99
        kelompok["awal" if nomor <= 7 else "lanjutan"].append(kr)

    hasil = []
    if kelompok["awal"]:
        hasil.append(("Keluhan umum", kelompok["awal"]))
    if kelompok["lanjutan"]:
        hasil.append(("Tanda lanjutan", kelompok["lanjutan"]))
    return hasil


def _proses_retrieve(nilai, nama):
    """
    Menjalankan Retrieve + Reuse dan menyimpan hasilnya di session_state.
    Mengembalikan True bila berhasil, None bila validasi gagal.
    """
    daftar_kriteria = svc_kriteria.daftar_kriteria()
    urutan = [k["kode"] for k in daftar_kriteria]

    error = validasi.validasi_teks(nama, "Nama atau kode pasien")
    if error is None:
        error = validasi.validasi_gejala_dipilih(nilai, daftar_kriteria)
    if error is None:
        error = validasi.validasi_vektor(cbr.bangun_vektor(nilai, urutan), len(urutan))
    if error:
        st.error(error)
        return None

    vektor_baru = cbr.bangun_vektor(nilai, urutan)
    data_kasus = svc_kasus.daftar_kasus()
    if len(data_kasus) == 0:
        st.error("Belum ada kasus pembanding di database.")
        return None

    kasus_lama = cbr.siapkan_kasus_lama(data_kasus, urutan)
    with st.spinner(f"Membandingkan dengan {len(kasus_lama)} kasus yang tersimpan..."):
        hasil = cbr.retrieve(vektor_baru, kasus_lama)

    rekomendasi = cbr.reuse(hasil)

    st.session_state["hasil_cbr"] = {
        "nama": nama.strip(),
        "nilai": dict(nilai),
        "vektor_baru": vektor_baru,
        "hasil": hasil,
        "rekomendasi": rekomendasi,
    }
    st.session_state.pop("revise_cbr", None)
    st.session_state.pop("retain_selesai", None)
    return True


def _tampilkan_hasil(hasil_cbr):
    """Panel hasil utama: persentase, kasus acuan, dan rekomendasi awal."""
    tema.bagian(
        "03",
        "Hasil Pemeriksaan",
        "Dibandingkan dengan seluruh kasus yang tersimpan.",
    )

    rekomendasi = hasil_cbr["rekomendasi"]
    if rekomendasi is None:
        st.warning("Tidak ada kasus pembanding, sehingga rekomendasi tidak tersedia.")
        return

    with st.container(border=True):
        kol_kiri, kol_kanan = st.columns([1, 1.8], gap="large")
        with kol_kiri:
            tema.gauge(
                rekomendasi["persentase"],
                f"ID {rekomendasi['kasus_id']} — {rekomendasi['nama']}",
                f"Cosine Similarity {round(rekomendasi['cosine'], 4)}",
            )
        with kol_kanan:
            st.markdown('<div class="card-kicker">Rekomendasi awal</div>', unsafe_allow_html=True)
            tema.judul_kartu(rekomendasi["solusi"])
            st.markdown(
                tema.meta_rows([
                    ("Kasus pembanding", rekomendasi["nama"]),
                    ("ID kasus", rekomendasi["kasus_id"]),
                    ("Tingkat kemiripan", f"{round(rekomendasi['persentase'], 2)} %"),
                ]),
                unsafe_allow_html=True,
            )
            st.caption(
                "Nilai ini dihitung dari dot product dan panjang kedua vektor. "
                "Rinciannya dapat dibuka di bawah."
            )

    tema.catatan(
        "Setiap gejala bernilai 1 bila dicentang dan 0 bila tidak. Nilai itulah "
        "yang dibandingkan dengan vektor kasus yang tersimpan."
    )

    st.caption("Tiga kasus pembanding terdekat")
    tema.peringkas([
        {
            "peringkat": h["peringkat"],
            "nama": h["nama"],
            "cosine": h["cosine"],
            "persentase": h["persentase"],
        }
        for h in hasil_cbr["hasil"][:3]
    ])

    with st.expander("Lihat langkah perhitungan"):
        st.write(f"**Vektor gejala Anda:** `{format_vektor(hasil_cbr['vektor_baru'])}`")
        st.dataframe(
            baris_tabel_perbandingan(hasil_cbr["hasil"]),
            width="stretch",
            hide_index=True,
        )

        for h in hasil_cbr["hasil"]:
            st.markdown(f"**ID {h['kasus_id']} — {h['nama']}** (peringkat {h['peringkat']})")
            st.code(
                "Vektor kasus     = "
                f"{format_vektor(h['vektor_lama'])}\n"
                "Dot product      = "
                f"{format_rincian_dot(hasil_cbr['vektor_baru'], h['vektor_lama'], h['rincian_dot'], h['dot_product'])}\n"
                "Panjang vektor   = "
                f"{round(h['panjang_baru'], 4)} (baru) × "
                f"{round(h['panjang_lama'], 4)} (kasus)\n"
                "Cosine Similarity = "
                f"{h['dot_product']} / ({round(h['panjang_baru'], 4)} × "
                f"{round(h['panjang_lama'], 4)}) = {round(h['cosine'], 4)}\n"
                "Kemiripan        = "
                f"{round(h['persentase'], 2)} %",
                language="text",
            )


def _tampilkan_revise(hasil_cbr):
    """Form peninjauan: terima rekomendasi atau tuliskan koreksi."""
    tema.bagian(
        "04",
        "Tinjau Rekomendasi",
        "Kosongkan kolom bila rekomendasi sudah tepat. Isi bila perlu koreksi.",
    )

    rekomendasi = hasil_cbr["rekomendasi"]
    if rekomendasi is None:
        st.info("Tidak ada rekomendasi yang perlu ditinjau.")
        return

    with st.container(border=True):
        kol_info, kol_form = st.columns([1, 1.6], gap="large")
        with kol_info:
            st.markdown(
                '<div class="card-kicker">Keputusan Anda</div>',
                unsafe_allow_html=True,
            )
            st.write(
                "Bandingkan rekomendasi sistem dengan kondisi pasien. Anda bisa "
                "menerimanya apa adanya atau menuliskan solusi akhir yang lebih tepat."
            )
            tema.catatan(
                "Kosongkan kolom solusi bila rekomendasi sudah tepat. Isi bila perlu koreksi."
            )
        with kol_form:
            with st.form("form_revise"):
                solusi_user = st.text_input(
                    "Solusi akhir (kosongkan untuk menerima rekomendasi)",
                    placeholder=f"Rekomendasi sistem: {rekomendasi['solusi']}",
                )
                catatan = st.text_area(
                    "Catatan peninjauan (opsional)",
                    placeholder="Tuliskan alasan bila ada koreksi",
                    height=76,
                )
                disubmit = st.form_submit_button("Simpan Koreksi")

    if disubmit:
        st.session_state["revise_cbr"] = cbr.revise(rekomendasi, solusi_user, catatan)
        st.session_state.pop("retain_selesai", None)
        st.rerun()

    if "revise_cbr" in st.session_state:
        hasil = st.session_state["revise_cbr"]
        if hasil["sumber"] == "rekomendasi":
            st.success(f"Rekomendasi diterima: **{hasil['solusi_final']}**")
        else:
            st.success(f"Koreksi tersimpan: **{hasil['solusi_final']}**")
        if hasil["catatan"]:
            st.caption(f"Catatan: {hasil['catatan']}")


def _tampilkan_retain(hasil_cbr):
    """Menyimpan kasus baru dan riwayat setelah hasil ditinjau."""
    tema.bagian(
        "05",
        "Simpan Hasil",
        "Kasus ini akan menjadi pembanding pada pemeriksaan berikutnya.",
    )

    if "revise_cbr" not in st.session_state:
        st.info("Tinjau rekomendasi terlebih dahulu sebelum menyimpan.")
        return

    hasil_revise = st.session_state["revise_cbr"]
    rekomendasi = hasil_cbr["rekomendasi"]
    sudah_simpan = "retain_selesai" in st.session_state

    with st.container(border=True):
        kol_info, kol_aksi = st.columns([1.6, 1], gap="large")
        with kol_info:
            st.markdown(
                '<div class="card-kicker">Yang akan disimpan</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                tema.meta_rows([
                    ("Pasien", hasil_cbr["nama"]),
                    ("Solusi akhir", hasil_revise["solusi_final"]),
                    ("Sumber solusi", hasil_revise["sumber"]),
                ]),
                unsafe_allow_html=True,
            )
        with kol_aksi:
            if not sudah_simpan and st.button(
                "Simpan Hasil Pemeriksaan", type="primary"
            ):
                payload = cbr.retain(
                    hasil_cbr["vektor_baru"],
                    hasil_cbr["nilai"],
                    hasil_cbr["nama"],
                    hasil_revise,
                    rekomendasi,
                )

                kasus_id = svc_kasus.tambah_kasus(
                    payload["nama"],
                    payload["solusi_final"],
                    f"Hasil pemeriksaan; acuan kasus ID {payload['kasus_acuan_id']} "
                    f"(cosine {round(payload['cosine'], 4)})",
                    payload["nilai"],
                )
                svc_riwayat.simpan_konsultasi({
                    "nama_kasus_baru": payload["nama"],
                    "vektor_baru": payload["vektor"],
                    "kasus_acuan_id": payload["kasus_acuan_id"],
                    "cosine_tertinggi": payload["cosine"],
                    "solusi_rekomendasi": rekomendasi["solusi"],
                    "solusi_final": payload["solusi_final"],
                    "sumber_solusi": payload["sumber_solusi"],
                    "catatan": payload["catatan"],
                    "detail": hasil_cbr["hasil"],
                })

                st.session_state["retain_selesai"] = kasus_id
                st.rerun()

    if sudah_simpan:
        st.success(
            f"Hasil pemeriksaan tersimpan. Kasus baru mendapat ID "
            f"{st.session_state['retain_selesai']}."
        )


_TAHAP_DATA = "Data"
_TAHAP_GEJALA = "Gejala"
_TAHAP_HASIL = "Hasil"


def _set_tahap(tahap):
    """Callback tombol: pindah tahap sebelum halaman dibangun ulang."""
    st.session_state["tahap_konsultasi"] = tahap


def _mulai_baru():
    """Callback 'Pemeriksaan Baru': membersihkan isian dan hasil sebelumnya."""
    for kunci in list(st.session_state.keys()):
        if kunci.startswith("gejala_") or kunci in (
            "hasil_cbr",
            "revise_cbr",
            "retain_selesai",
            "nama_pasien",
            "input_nama_pasien",
        ):
            st.session_state.pop(kunci, None)
    st.session_state["tahap_konsultasi"] = _TAHAP_DATA


def _tampilkan_data():
    """Langkah 1: identitas pasien. Satu pertanyaan utama per layar."""
    with st.container(border=True):
        st.markdown(
            '<div class="card-kicker">Langkah 1 dari 2</div>',
            unsafe_allow_html=True,
        )
        tema.judul_kartu("Siapa yang akan diperiksa?", besar=True)
        st.caption("Nama atau kode ini dipakai sebagai label pada Riwayat.")
        st.session_state.setdefault(
            "input_nama_pasien", st.session_state.get("nama_pasien", "")
        )
        with st.form("form_data_pasien"):
            nama = st.text_input(
                "Nama atau kode pasien",
                key="input_nama_pasien",
                placeholder="cth: Pasien 01",
                help="Gunakan nama atau kode yang mudah dikenali.",
            )
            disubmit = st.form_submit_button("Lanjut", type="primary")

    if disubmit:
        error = validasi.validasi_teks(nama, "Nama atau kode pasien")
        if error:
            st.error(error)
        else:
            st.session_state["nama_pasien"] = nama.strip()
            st.session_state["tahap_konsultasi"] = _TAHAP_GEJALA
            st.rerun()


def _tampilkan_gejala():
    """Langkah 2: centang gejala, lalu jalankan Retrieve dan Reuse."""
    daftar_kriteria = svc_kriteria.daftar_kriteria()
    tersimpan = st.session_state.get("gejala_terpilih", {})
    nama = st.session_state.get("nama_pasien", "")

    with st.container(border=True):
        st.markdown(
            '<div class="card-kicker">Langkah 2 dari 2</div>',
            unsafe_allow_html=True,
        )
        tema.judul_kartu("Gejala apa yang Anda rasakan?", besar=True)
        st.caption(f"Pasien: {nama}. Centang semua keluhan yang sesuai.")

        if len(daftar_kriteria) == 0:
            st.info("Daftar gejala belum tersedia.")
            st.button("Kembali", on_click=_set_tahap, args=(_TAHAP_DATA,))
            return

        with st.form("form_cek_gejala"):
            nilai = {}
            for indeks, (judul_grup, kriteria_grup) in enumerate(
                _kelompokkan_gejala(daftar_kriteria)
            ):
                if indeks > 0:
                    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
                tema.grup_gejala(judul_grup)
                kolom_pilihan = st.columns(2)
                for i, kr in enumerate(kriteria_grup):
                    kunci = f"gejala_{kr['kode']}"
                    # Centang dipulihkan bila pengguna kembali dari hasil.
                    st.session_state.setdefault(
                        kunci, bool(tersimpan.get(kr["kode"], 0))
                    )
                    dicentang = kolom_pilihan[i % 2].checkbox(kr["nama"], key=kunci)
                    nilai[kr["kode"]] = 1 if dicentang else 0

            st.markdown('<hr class="hairline">', unsafe_allow_html=True)
            submitted = st.form_submit_button("Periksa Sekarang", type="primary")

        st.button("Kembali", on_click=_set_tahap, args=(_TAHAP_DATA,))

    if submitted:
        st.session_state["gejala_terpilih"] = dict(nilai)
        if _proses_retrieve(nilai, nama):
            st.session_state["tahap_konsultasi"] = _TAHAP_HASIL
            st.rerun()


def _tampilkan_hasil_utama():
    """Langkah 3-4: hasil, tinjau, dan simpan."""
    hasil_cbr = st.session_state["hasil_cbr"]
    st.write(f"**Memeriksa:** {hasil_cbr['nama']}")
    terpilih = [
        kr["nama"]
        for kr in svc_kriteria.daftar_kriteria()
        if hasil_cbr["nilai"].get(kr["kode"]) == 1
    ]
    tema.pil_ringkas(terpilih, "Gejala yang Anda pilih")
    st.markdown('<hr class="hairline">', unsafe_allow_html=True)

    _tampilkan_hasil(hasil_cbr)
    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    _tampilkan_revise(hasil_cbr)
    st.markdown('<hr class="hairline">', unsafe_allow_html=True)
    _tampilkan_retain(hasil_cbr)

    st.divider()
    kol_ubah, kol_baru = st.columns(2)
    with kol_ubah:
        st.button("Ubah Gejala", on_click=_set_tahap, args=(_TAHAP_GEJALA,))
    with kol_baru:
        st.button("Pemeriksaan Baru", on_click=_mulai_baru)


def tampilkan():
    tema.header(
        "Cek Gejala",
        "Isi data singkat, pilih gejala yang Anda alami, lalu lihat perbandingan "
        "dengan kasus yang sudah tercatat.",
        eyebrow="Pemeriksaan",
    )
    tahap = st.session_state.get("tahap_konsultasi", _TAHAP_DATA)
    if tahap == _TAHAP_HASIL and "hasil_cbr" not in st.session_state:
        tahap = _TAHAP_DATA

    if tahap == _TAHAP_HASIL:
        sudah_ditinjau = (
            "revise_cbr" in st.session_state or "retain_selesai" in st.session_state
        )
        tema.langkah_cbr("Hasil" if sudah_ditinjau else "Analisis")
    else:
        tema.langkah_cbr(tahap)

    tema.catatan(
        "Pemeriksaan ini membantu membaca kemungkinan berdasarkan kasus yang "
        "sudah tercatat. Hasilnya bukan diagnosis medis final."
    )

    if tahap == _TAHAP_DATA:
        _tampilkan_data()
    elif tahap == _TAHAP_GEJALA:
        _tampilkan_gejala()
    else:
        _tampilkan_hasil_utama()
