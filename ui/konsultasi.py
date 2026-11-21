"""
Halaman Konsultasi Baru: alur lengkap tahapan CBR.

    1. Retrieve  -> perhitungan Cosine Similarity manual terhadap semua kasus
    2. Reuse     -> solusi kasus paling mirip sebagai rekomendasi awal
    3. Revise    -> user meninjau/mengoreksi rekomendasi
    4. Retain    -> kasus baru + solusi final disimpan ke database

Hasil perhitungan disimpan di st.session_state["hasil_cbr"] agar tetap ada
saat Streamlit menjalankan ulang script (rerun) setiap kali user berinteraksi.
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
    tampilkan_flash,
)


def _proses_retrieve(nilai, nama_kasus):
    """
    Menjalankan Retrieve + Reuse, lalu menyimpan hasilnya di session_state.
    Mengembalikan None bila validasi gagal (pesan error sudah ditampilkan).
    """
    kriteria = svc_kriteria.daftar_kriteria()
    urutan = [k["kode"] for k in kriteria]

    error = validasi.validasi_teks(nama_kasus, "Nama kasus baru")
    if error is None:
        error = validasi.validasi_gejala_dipilih(nilai, kriteria)
    if error is None:
        error = validasi.validasi_vektor(cbr.bangun_vektor(nilai, urutan), len(urutan))
    if error:
        st.error(error)
        return None

    # --- RETRIEVE --------------------------------------------------------
    vektor_baru = cbr.bangun_vektor(nilai, urutan)
    daftar_kasus = svc_kasus.daftar_kasus()

    if len(daftar_kasus) == 0:
        st.error("Belum ada kasus pembanding. Tambahkan kasus dulu di halaman Kasus.")
        return None

    kasus_lama = cbr.siapkan_kasus_lama(daftar_kasus, urutan)
    with st.spinner(f"Membandingkan kasus baru dengan {len(kasus_lama)} kasus lama..."):
        hasil = cbr.retrieve(vektor_baru, kasus_lama)

    # --- REUSE -----------------------------------------------------------
    rekomendasi = cbr.reuse(hasil)

    st.session_state["hasil_cbr"] = {
        "nama_kasus_baru": nama_kasus.strip(),
        "nilai": dict(nilai),
        "vektor_baru": vektor_baru,
        "urutan_kode": urutan,
        "hasil": hasil,
        "rekomendasi": rekomendasi,
    }
    # Proses baru membuat hasil Revise/Retain sebelumnya tidak berlaku lagi.
    st.session_state.pop("revise_cbr", None)
    st.session_state.pop("retain_selesai", None)
    return True


def _tampilkan_retrieve(hasil_cbr):
    """Menampilkan tahap Retrieve: tabel perbandingan + detail per kasus."""
    tema.bagian(
        "🔎",
        "1. Retrieve — Pencarian Kasus Paling Mirip",
        "Kasus baru dibandingkan dengan SELURUH kasus lama memakai Cosine "
        "Similarity yang dihitung manual (lihat modul core/cosine.py).",
        badge="Tahap 1",
        badge_tone="biru",
    )

    st.write(f"**Vektor kasus baru:** `{format_vektor(hasil_cbr['vektor_baru'])}`")
    if len(hasil_cbr["hasil"]) > 0:
        contoh = hasil_cbr["hasil"][0]
        st.write(
            f"**Jumlah kuadrat kasus baru:** {contoh['jumlah_kuadrat_baru']} "
            f"→ panjang vektor = {round(contoh['panjang_baru'], 4)}"
        )

    st.dataframe(
        baris_tabel_perbandingan(hasil_cbr["hasil"]),
        width="stretch",
        hide_index=True,
    )

    # Detail langkah per kasus agar user memahami asal angka cosine.
    with st.expander("Lihat langkah perhitungan tiap kasus"):
        vektor_baru = hasil_cbr["vektor_baru"]
        for h in hasil_cbr["hasil"]:
            st.markdown(
                f"**Kasus ID {h['kasus_id']} — {h['nama']}** "
                f"(peringkat {h['peringkat']})"
            )
            st.code(
                "Vektor lama        = "
                f"{format_vektor(h['vektor_lama'])}\n"
                "Dot product        = "
                f"{format_rincian_dot(vektor_baru, h['vektor_lama'], h['rincian_dot'], h['dot_product'])}\n"
                "Jumlah kuadrat baru = "
                f"{h['jumlah_kuadrat_baru']} → panjang = "
                f"{round(h['panjang_baru'], 4)}\n"
                "Jumlah kuadrat lama = "
                f"{h['jumlah_kuadrat_lama']} → panjang = "
                f"{round(h['panjang_lama'], 4)}\n"
                "Cosine = "
                f"{h['dot_product']} / ({round(h['panjang_baru'], 4)} x "
                f"{round(h['panjang_lama'], 4)}) = {round(h['cosine'], 4)}\n"
                "Kemiripan = "
                f"{round(h['persentase'], 2)} %",
                language="text",
            )


def _tampilkan_reuse(rekomendasi):
    """Menampilkan tahap Reuse: solusi awal dari kasus terdekat."""
    tema.bagian(
        "♻️",
        "2. Reuse — Pengambilan Solusi Awal",
        "Solusi kasus dengan kemiripan tertinggi dipakai sebagai rekomendasi "
        "awal untuk kasus baru.",
        badge="Tahap 2",
        badge_tone="hijau",
    )

    if rekomendasi is None:
        st.warning("Tidak ada kasus pembanding, sehingga tidak ada rekomendasi.")
        return

    st.info(
        f"**Kasus paling mirip:** ID {rekomendasi['kasus_id']} — "
        f"{rekomendasi['nama']}\n\n"
        f"**Cosine Similarity:** {round(rekomendasi['cosine'], 4)} "
        f"({round(rekomendasi['persentase'], 2)} %)\n\n"
        f"**Rekomendasi solusi:** {rekomendasi['solusi']}"
    )


def _tampilkan_revise(hasil_cbr):
    """Menampilkan tahap Revise: form tinjauan solusi."""
    tema.bagian(
        "✍️",
        "3. Revise — Peninjauan Solusi",
        "User meninjau rekomendasi. Kosongkan kolom solusi jika rekomendasi "
        "diterima; isi bila perlu koreksi. Hasil akhir menjadi solusi final.",
        badge="Tahap 3",
        badge_tone="kuning",
    )

    rekomendasi = hasil_cbr["rekomendasi"]
    if rekomendasi is None:
        st.warning("Tidak ada rekomendasi untuk ditinjau.")
        return

    with st.form("form_revise"):
        solusi_user = st.text_input(
            "Solusi final (kosongkan untuk menerima rekomendasi)",
            value="",
            placeholder=f"Rekomendasi sistem: {rekomendasi['solusi']}",
        )
        catatan = st.text_area(
            "Catatan peninjauan (opsional)",
            placeholder="cth: gejala tambahan belum tercatat, sesuaikan diagnosis",
            height=80,
        )
        submitted = st.form_submit_button("Validasi Solusi (Revise)")

    if submitted:
        hasil_revise = cbr.revise(rekomendasi, solusi_user, catatan)
        st.session_state["revise_cbr"] = hasil_revise
        st.session_state.pop("retain_selesai", None)

    # Tampilkan status validasi bila sudah pernah disubmit.
    if "revise_cbr" in st.session_state:
        hasil_revise = st.session_state["revise_cbr"]
        if hasil_revise["sumber"] == "rekomendasi":
            st.success(
                "Solusi diterima dari rekomendasi sistem: "
                f"**{hasil_revise['solusi_final']}**"
            )
        else:
            st.success(
                "Solusi hasil koreksi user: "
                f"**{hasil_revise['solusi_final']}**"
            )
        if hasil_revise["catatan"]:
            st.caption(f"Catatan: {hasil_revise['catatan']}")


def _tampilkan_retain(hasil_cbr):
    """Menampilkan tahap Retain: tombol simpan kasus baru + riwayat."""
    tema.bagian(
        "💾",
        "4. Retain — Penyimpanan Kasus Baru",
        "Kasus baru beserta solusi final disimpan agar menjadi pembanding "
        "pada konsultasi berikutnya, dan riwayat perhitungan ikut tercatat.",
        badge="Tahap 4",
        badge_tone="abu",
    )

    if "revise_cbr" not in st.session_state:
        st.info("Selesaikan tahap Revise terlebih dahulu.")
        return

    # `sudah_retain` dipakai agar pesan sukses langsung muncul pada run yang
    # sama saat tombol diklik, dan tombol tidak menampilkan pesan ganda.
    sudah_retain = "retain_selesai" in st.session_state

    if not sudah_retain:
        if st.button("Simpan Kasus Baru & Riwayat (Retain)", type="primary"):
            hasil_revise = st.session_state["revise_cbr"]
            rekomendasi = hasil_cbr["rekomendasi"]

            # Menyiapkan payload lalu menyimpan ke database (lihat core/cbr.py).
            payload = cbr.retain(
                hasil_cbr["vektor_baru"],
                hasil_cbr["nilai"],
                hasil_cbr["nama_kasus_baru"],
                hasil_revise,
                rekomendasi,
            )

            kasus_id = svc_kasus.tambah_kasus(
                payload["nama"],
                payload["solusi_final"],
                f"Disimpan otomatis dari konsultasi; acuan kasus ID "
                f"{payload['kasus_acuan_id']} "
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
            sudah_retain = True

    if sudah_retain:
        st.success(
            "Retain berhasil! Kasus baru (ID "
            f"{st.session_state['retain_selesai']}) dan riwayat konsultasi "
            "tersimpan di database."
        )
        st.caption(
            "Kasus ini otomatis menjadi pembanding pada konsultasi berikutnya."
        )


def tampilkan():
    tema.header(
        "🩺",
        "Konsultasi Baru",
        "Masukkan gejala kasus baru, lalu ikuti empat tahapan CBR.",
        badge="Input → Retrieve → Reuse → Revise → Retain",
        badge_tone="hijau",
    )
    tampilkan_flash()

    # Penanda progres mengikuti session_state, sehingga tetap benar setelah
    # Streamlit menjalankan ulang script saat user menekan tombol.
    tahap_aktif = "Retrieve"
    if "retain_selesai" in st.session_state:
        tahap_aktif = "Retain"
    elif "revise_cbr" in st.session_state:
        tahap_aktif = "Revise"
    elif "hasil_cbr" in st.session_state:
        tahap_aktif = "Reuse"
    tema.langkah_cbr(tahap_aktif)

    kriteria = svc_kriteria.daftar_kriteria()
    if len(kriteria) == 0:
        st.warning("Belum ada kriteria. Tambahkan kriteria di halaman Kriteria.")
        return

    # --- Form input kasus baru ------------------------------------------
    with st.container(border=True):
        st.markdown(
            '<span class="spk-badge biru">Langkah 0 · Input Kasus</span>',
            unsafe_allow_html=True,
        )
        with st.form("form_input_kasus_baru"):
            nama_kasus = st.text_input(
                "Nama / ID Kasus Baru", placeholder="cth: Pasien Baru 01"
            )
            st.caption(
                "Centang gejala yang muncul. Urutan vektor mengikuti urutan "
                "kriteria pada halaman Manajemen Kriteria."
            )
            st.write("**Pilih gejala yang muncul:**")
            nilai = {}
            kolom_gejala = st.columns(3)
            for i, kr in enumerate(kriteria):
                dicentang = kolom_gejala[i % 3].checkbox(
                    kr["nama"], key=f"kons_{kr['kode']}"
                )
                nilai[kr["kode"]] = 1 if dicentang else 0

            submitted = st.form_submit_button("Proses CBR (Retrieve + Reuse)")

    if submitted:
        _proses_retrieve(nilai, nama_kasus)

    # --- Tampilkan hasil bila sudah pernah diproses ----------------------
    if "hasil_cbr" not in st.session_state:
        st.info("Isi form di atas lalu tekan **Proses CBR** untuk memulai.")
        return

    hasil_cbr = st.session_state["hasil_cbr"]
    st.divider()
    st.write(
        f"**Memproses kasus:** {hasil_cbr['nama_kasus_baru']} — "
        f"vektor `{format_vektor(hasil_cbr['vektor_baru'])}`"
    )

    # Ringkasan eksekutif muncul lebih dulu agar user langsung melihat hasil.
    rekomendasi = hasil_cbr["rekomendasi"]
    if rekomendasi is not None:
        with st.container(border=True):
            st.markdown(
                '<span class="spk-badge hijau">Kasus Paling Mirip</span>',
                unsafe_allow_html=True,
            )
            tema.gauge(
                rekomendasi["persentase"],
                f"ID {rekomendasi['kasus_id']} — {rekomendasi['nama']}",
                f"Rekomendasi awal: {rekomendasi['solusi']}",
            )

    with st.container(border=True):
        _tampilkan_retrieve(hasil_cbr)
    with st.container(border=True):
        _tampilkan_reuse(hasil_cbr["rekomendasi"])
    with st.container(border=True):
        _tampilkan_revise(hasil_cbr)
    with st.container(border=True):
        _tampilkan_retain(hasil_cbr)

    # --- Tombol reset untuk memulai konsultasi baru ----------------------
    st.divider()
    if st.button("Mulai Ulang Konsultasi Baru"):
        for kunci in ("hasil_cbr", "revise_cbr", "retain_selesai"):
            st.session_state.pop(kunci, None)
        st.rerun()
