"""
Streamlit Web Application Entry Point: Prototype Deteksi Hate Speech Bahasa Indonesia.
"""

import os
import sys

# Tambahkan project root ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import streamlit as st
    from app.components.input_view import render_input_view
    from app.components.prediction_view import render_prediction_view
    from app.components.explanation_view import render_explanation_view
    from src.preprocessing.cleaner import TextCleaner
    from src.preprocessing.tokenizer import TextTokenizer
    from src.preprocessing.padder import SequencePadder
    from src.models.cnn_model import CNNTextClassifier
    from src.explainability.saliency import SaliencyMapper
    from src.utils.config import Config

    st.set_page_config(
        page_title="Indonesian Hate Speech Analyzer (Kelompok 4)",
        page_icon="🔍",
        layout="wide",
    )

    st.title("🔍 Indonesian Hate Speech Analyzer")
    st.caption("Kelompok 4: Convolutional Neural Network (CNN) for Text Classification")

    cfg = Config()
    cleaner = TextCleaner()

    text, btn_clicked = render_input_view()
    if btn_clicked and text:
        cleaned_text = cleaner.clean(text)
        st.write(f"**Teks Setelah Pembersihan:** `{cleaned_text}`")

        # Mock / Real inference skeleton
        confidence = 0.88
        pred_label = "⚠️ Hate Speech / Toxic" if confidence > 0.5 else "✅ Non-toxic"
        severity = "High" if confidence > 0.75 else "Medium"

        render_prediction_view(pred_label, confidence, severity)

        # Mock Saliency
        dummy_scores = [(w, 0.45 if i % 2 == 1 else 0.05) for i, w in enumerate(cleaned_text.split())]
        render_explanation_view(dummy_scores)

except ImportError as e:
    print(f"Library belum lengkap: {e}. Silakan instal requirements.txt.")
