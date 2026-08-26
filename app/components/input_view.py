from typing import Tuple


def render_input_view() -> Tuple[str, bool]:
    """
    Menampilkan form input teks pada halaman Streamlit.

    Returns:
        Tuple[str, bool]: (teks_input, tombol_submit_ditekan)
    """
    try:
        import streamlit as st

        st.subheader("📝 Input Teks Ujaran")
        text_input = st.text_area(
            "Masukkan teks bahasa Indonesia untuk dianalisis:",
            height=120,
            placeholder="Ketik atau paste teks di sini...",
        )
        submitted = st.button("🚀 Analisis Teks", use_container_width=True)
        return text_input, submitted
    except ImportError:
        return "", False
