"""
Halaman Manajemen Kasus: tambah, lihat, ubah, dan hapus kasus lama.

Formulir kasus berupa centang gejala (0/1) sesuai daftar kriteria,
sehingga nilai tersimpan per kriteria dan mudah diperluas di masa depan.
"""

import streamlit as st

from services import kasus as svc_kasus
from services import kriteria as svc_kriteria
from services import validasi
from ui import tema
from ui.helper import baris_gejala, set_flash, tampilkan_flash


def _form_gejala(prefix, nilai_awal):
    """
    Menampilkan centang gejala dan mengembalikan dict {kode: 0/1}.
    `prefix` membuat key widget unik antar mode tambah/ubah.
    """
    nilai = {}
    kolom = st.columns(3)
    for i, kr in enumerate(svc_kriteria.daftar_kriteria()):
        dicentang = kolom[i % 3].checkbox(
            kr["nama"],
            value=bool(nilai_awal.get(kr["kode"], 0)),
            key=f"{prefix}_{kr['kode']}",
        )
        nilai[kr["kode"]] = 1 if dicentang else 0
    return nilai


def tampilkan():
    tema.header(
        "🗂️",
        "Manajemen Kasus",
        "Kasus lama adalah basis pengetahuan CBR: gejala (vektor) + solusi. "
        "Semakin banyak kasus, semakin kaya pembanding saat Retrieve.",
        badge="Basis Pengetahuan",
        badge_tone="hijau",
    )
    tampilkan_flash()

    daftar = svc_kriteria.daftar_kriteria()
    if len(daftar) == 0:
        st.warning("Belum ada kriteria. Tambahkan kriteria di halaman Kriteria.")
        return

    daftar_kasus = svc_kasus.daftar_kasus()

    # Ringkasan kecil supaya user langsung melihat isi basis pengetahuan.
    total_gejala_aktif = 0
    for k in daftar_kasus:
        for nilai_gejala in k["nilai"].values():
            if nilai_gejala == 1:
                total_gejala_aktif += 1
    rata_rata = 0
    if len(daftar_kasus) > 0:
        rata_rata = round(total_gejala_aktif / len(daftar_kasus), 1)

    kartu1, kartu2, kartu3 = st.columns(3)
    with kartu1:
        tema.kartu_ringkas("Total Kasus", len(daftar_kasus), "kasus pembanding")
    with kartu2:
        tema.kartu_ringkas("Gejala Tersedia", len(daftar), "kriteria aktif")
    with kartu3:
        tema.kartu_ringkas("Rata-rata Gejala", rata_rata, "per kasus")
    st.divider()

    # --- Tambah kasus ----------------------------------------------------
    tema.bagian("➕", "Tambah Kasus Baru", badge="Input Basis Pengetahuan", badge_tone="biru")
    with st.container(border=True):
        with st.form("form_tambah_kasus"):
            kol_nama, kol_solusi = st.columns(2)
            nama = kol_nama.text_input("Nama Kasus", placeholder="cth: Pasien A")
            solusi = kol_solusi.text_input(
                "Solusi / Diagnosis", placeholder="cth: DBD Fase Awal"
            )
            keterangan = st.text_area("Keterangan (opsional)", height=80)
            st.caption(
                "Centang gejala sesuai daftar kriteria; urutan vektor mengikuti "
                "urutan kriteria pada halaman Manajemen Kriteria."
            )
            st.write("**Gejala yang muncul:**")
            nilai = _form_gejala("baru", {})
            submitted = st.form_submit_button("Simpan Kasus")

    if submitted:
        error = validasi.validasi_teks(nama, "Nama kasus")
        if error is None:
            error = validasi.validasi_teks(solusi, "Solusi")
        if error is None:
            error = validasi.validasi_gejala_dipilih(nilai, daftar)

        if error:
            st.error(error)
        else:
            svc_kasus.tambah_kasus(nama, solusi, keterangan, nilai)
            set_flash(f"Kasus '{nama.strip()}' berhasil disimpan.")
            st.rerun()

    st.divider()

    # --- Daftar kasus ----------------------------------------------------
    tema.bagian(
        "🗃️",
        f"Daftar Kasus ({len(daftar_kasus)} kasus)",
        badge="Kasus Tersimpan",
        badge_tone="abu",
    )
    if len(daftar_kasus) == 0:
        st.info("Belum ada kasus tersimpan.")
        return

    for k in daftar_kasus:
        jumlah_gejala = 0
        for v in k["nilai"].values():
            if v == 1:
                jumlah_gejala += 1

        with st.expander(
            f"ID {k['id']} — {k['nama']} | Solusi: {k['solusi']} "
            f"| Gejala aktif: {jumlah_gejala}/{len(daftar)}"
        ):
            st.write(f"**Keterangan:** {k['keterangan'] or '-'}")
            st.caption(f"Dibuat: {k['dibuat_pada']}")
            st.dataframe(
                baris_gejala(k["nilai"]),
                width="stretch",
                hide_index=True,
            )

            # --- Ubah kasus ---------------------------------------------
            with st.form(f"form_ubah_kasus_{k['id']}"):
                st.markdown("**Ubah kasus ini**")
                kol_nama_ubah, kol_solusi_ubah = st.columns(2)
                nama_ubah = kol_nama_ubah.text_input(
                    "Nama Kasus", value=k["nama"], key=f"n_{k['id']}"
                )
                solusi_ubah = kol_solusi_ubah.text_input(
                    "Solusi / Diagnosis", value=k["solusi"], key=f"s_{k['id']}"
                )
                keterangan_ubah = st.text_area(
                    "Keterangan", value=k["keterangan"] or "", key=f"k_{k['id']}"
                )
                st.write("**Gejala:**")
                nilai_ubah = _form_gejala(f"ubah{k['id']}", k["nilai"])

                kol_simpan, kol_hapus = st.columns(2)
                tombol_simpan = kol_simpan.form_submit_button("Simpan Perubahan")
                tombol_hapus = kol_hapus.form_submit_button("Hapus Kasus")

            if tombol_simpan:
                error = validasi.validasi_teks(nama_ubah, "Nama kasus")
                if error is None:
                    error = validasi.validasi_teks(solusi_ubah, "Solusi")
                if error is None:
                    error = validasi.validasi_gejala_dipilih(nilai_ubah, daftar)

                if error:
                    st.error(error)
                else:
                    svc_kasus.ubah_kasus(
                        k["id"], nama_ubah, solusi_ubah, keterangan_ubah, nilai_ubah
                    )
                    set_flash("Kasus berhasil diubah.")
                    st.rerun()

            if tombol_hapus:
                svc_kasus.hapus_kasus(k["id"])
                set_flash(f"Kasus '{k['nama']}' berhasil dihapus.")
                st.rerun()
