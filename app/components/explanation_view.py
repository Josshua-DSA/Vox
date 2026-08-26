from typing import List, Tuple


def render_explanation_view(
    saliency_scores: List[Tuple[str, float]]
) -> None:
    """
    Menampilkan highlight kata dengan intensitas warna sesuai bobot saliency.

    Args:
        saliency_scores (List[Tuple[str, float]]): Daftar pasangan (kata, skor).
    """
    try:
        import streamlit as st

        st.subheader("💡 Explainability (Feature Saliency Highlight)")
        if not saliency_scores:
            st.info("Belum ada data visualisasi atribusi kata.")
            return

        html_tokens = []
        for word, score in saliency_scores:
            # Color intensity alpha based on score
            alpha = min(1.0, score * 2.5)
            if score > 0.1:
                bg_color = f"rgba(231, 76, 60, {alpha:.2f})"
                html_tokens.append(
                    f'<span style="background-color: {bg_color}; padding: 2px 6px; margin: 2px; border-radius: 4px; font-weight: bold;" title="Saliency: {score:.4f}">{word}</span>'
                )
            else:
                html_tokens.append(f'<span style="padding: 2px 4px;">{word}</span>')

        rendered_html = " ".join(html_tokens)
        st.markdown(
            f'<div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; font-size: 1.1em; line-height: 2.0;">{rendered_html}</div>',
            unsafe_allow_html=True,
        )
    except ImportError:
        pass
