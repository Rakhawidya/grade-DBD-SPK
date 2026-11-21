"""
Halaman Manajemen Kriteria (gejala/atribut).

Kriteria menentukan jumlah elemen vektor, sehingga halaman ini juga
menjelaskan konsekuensi penghapusan kriteria kepada user.
"""

import streamlit as st

from services import kriteria as svc_kriteria
from services import validasi
from ui import tema
from ui.helper import set_flash, tampilkan_flash


def tampilkan():
    tema.header(
        "⚙️",
        "Manajemen Kriteria",
        "Kriteria adalah gejala/atribut yang menjadi isi vektor kasus. "
        "Urutan kriteria menentukan urutan angka pada vektor.",
        badge="Urutan Vektor",
        badge_tone="biru",
    )
    tampilkan_flash()

    daftar = svc_kriteria.daftar_kriteria()

    kartu1, kartu2, kartu3 = st.columns(3)
    with kartu1:
        tema.kartu_ringkas(
            "Kriteria Terdaftar",
            len(daftar),
            "Jumlah elemen pada setiap vektor kasus",
        )
    with kartu2:
        tema.kartu_ringkas(
            "Kode Pertama",
            daftar[0]["kode"] if daftar else "-",
            "Elemen pertama pada vektor",
        )
    with kartu3:
        tema.kartu_ringkas(
            "Kode Terakhir",
            daftar[-1]["kode"] if daftar else "-",
            "Elemen terakhir pada vektor",
        )
    st.divider()

    # Dua kolom: kiri untuk tambah, kanan untuk ubah/hapus.
    # Kolom kiri tetap tampil walaupun daftar kosong, supaya kriteria pertama
    # tetap bisa ditambahkan dari halaman ini.
    kol_tambah, kol_ubah = st.columns([1, 1], gap="large")

    # --- Tambah kriteria -------------------------------------------------
    with kol_tambah:
        with st.container(border=True):
            st.markdown(
                '<span class="spk-badge biru">Tambah Baru</span>',
                unsafe_allow_html=True,
            )
            st.subheader("Tambah Kriteria")
            with st.form("form_tambah_kriteria", clear_on_submit=True):
                kol_kode, kol_nama = st.columns([1, 3])
                kode = kol_kode.text_input(
                    "Kode", placeholder="cth: G15", key="kriteria_kode_baru"
                )
                nama = kol_nama.text_input(
                    "Nama Gejala",
                    placeholder="cth: Nyeri sendi",
                    key="kriteria_nama_baru",
                )
                submitted = st.form_submit_button("Simpan Kriteria")

        if submitted:
            error = validasi.validasi_teks(nama, "Nama gejala")
            if error is None:
                error = validasi.validasi_kode_kriteria(kode, daftar)

            if error:
                st.error(error)
            else:
                try:
                    svc_kriteria.tambah_kriteria(kode, nama)
                except ValueError as pesan:
                    st.error(str(pesan))
                else:
                    set_flash(f"Kriteria {kode.strip().upper()} berhasil ditambahkan.")
                    st.rerun()

    # --- Ubah / hapus kriteria -------------------------------------------
    with kol_ubah:
        if len(daftar) == 0:
            with st.container(border=True):
                st.markdown(
                    '<span class="spk-badge abu">Belum Ada Data</span>',
                    unsafe_allow_html=True,
                )
                st.subheader("Ubah atau Hapus Kriteria")
                st.info(
                    "Belum ada kriteria. Tambahkan kriteria pertama "
                    "melalui form di sebelah kiri."
                )
        else:
            with st.container(border=True):
                st.markdown(
                    '<span class="spk-badge kuning">Perbarui Data</span>',
                    unsafe_allow_html=True,
                )
                st.subheader("Ubah atau Hapus Kriteria")
                pilihan = {f"{k['kode']} - {k['nama']}": k for k in daftar}
                nama_pilihan = st.selectbox("Pilih kriteria", list(pilihan.keys()))
                kriteria_terpilih = pilihan[nama_pilihan]

                with st.form("form_ubah_kriteria"):
                    kol_kode2, kol_nama2 = st.columns([1, 3])
                    # Key memakai id kriteria supaya field ikut berganti saat user
                    # memilih kriteria lain (nilai lama tidak tertinggal).
                    kode_baru = kol_kode2.text_input(
                        "Kode",
                        value=kriteria_terpilih["kode"],
                        key=f"kriteria_kode_{kriteria_terpilih['id']}",
                    )
                    nama_baru = kol_nama2.text_input(
                        "Nama Gejala",
                        value=kriteria_terpilih["nama"],
                        key=f"kriteria_nama_{kriteria_terpilih['id']}",
                    )
                    kol_simpan, kol_hapus = st.columns(2)
                    tombol_simpan = kol_simpan.form_submit_button("Simpan Perubahan")
                    tombol_hapus = kol_hapus.form_submit_button("Hapus Kriteria")

            if tombol_simpan:
                error = validasi.validasi_teks(nama_baru, "Nama gejala")
                if error is None:
                    error = validasi.validasi_kode_kriteria(
                        kode_baru, daftar, kriteria_id=kriteria_terpilih["id"]
                    )

                if error:
                    st.error(error)
                else:
                    try:
                        svc_kriteria.ubah_kriteria(
                            kriteria_terpilih["id"], kode_baru, nama_baru
                        )
                    except ValueError as pesan:
                        st.error(str(pesan))
                    else:
                        set_flash("Kriteria berhasil diubah.")
                        st.rerun()

            if tombol_hapus:
                try:
                    svc_kriteria.hapus_kriteria(kriteria_terpilih["id"])
                except ValueError as pesan:
                    # Ditolak bila kriteria sudah dipakai kasus (menjaga integritas vektor)
                    st.error(str(pesan))
                else:
                    set_flash(f"Kriteria {kriteria_terpilih['kode']} berhasil dihapus.")
                    st.rerun()

    st.divider()

    # --- Tabel daftar kriteria ------------------------------------------
    tema.bagian(
        "📋",
        f"Daftar Kriteria ({len(daftar)} gejala)",
        "Urutan pada tabel ini adalah urutan angka di dalam vektor kasus.",
        badge="Daftar Gejala",
        badge_tone="abu",
    )
    if len(daftar) == 0:
        st.info("Belum ada kriteria tersimpan.")
        return

    st.dataframe(
        [
            {"ID": k["id"], "Kode": k["kode"], "Nama": k["nama"], "Urutan": k["urutan"]}
            for k in daftar
        ],
        width="stretch",
        hide_index=True,
    )
