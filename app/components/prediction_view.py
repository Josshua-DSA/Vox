def render_prediction_view(
    prediction_label: str, confidence: float, severity: str
) -> None:
    """
    Menampilkan visualisasi kartu hasil prediksi klasifikasi.

    Args:
        prediction_label (str): Label ("Hate Speech / Toxic" atau "Non-toxic").
        confidence (float): Tingkat keyakinan model [0.0 - 1.0].
        severity (str): Tingkat keparahan ("Low", "Medium", "High").
    """
    try:
        import streamlit as st

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🎯 Prediksi", value=prediction_label)
        with col2:
            st.metric(label="📊 Confidence", value=f"{confidence * 100:.2f}%")
        with col3:
            st.metric(label="⚠️ Severity", value=severity)
    except ImportError:
        pass
