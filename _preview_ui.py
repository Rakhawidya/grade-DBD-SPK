"""Harness sementara untuk pemeriksaan visual lewat query parameter."""

from pathlib import Path

import streamlit as st

_sumber = Path(__file__).with_name("app.py").read_text(encoding="utf-8")
_suntikan = (
    'st.session_state["halaman_tujuan"] = st.query_params.get("page", "Beranda")\n'
    "tema.terapkan_tema()"
)
_sumber = _sumber.replace("tema.terapkan_tema()", _suntikan, 1)

exec(compile(_sumber, str(Path(__file__).with_name("app.py")), "exec"), {
    "__name__": "__main__",
    "__file__": str(Path(__file__).with_name("app.py")),
})
