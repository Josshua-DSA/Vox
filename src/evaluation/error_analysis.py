import json
import os
from typing import Any, Dict, List
import pandas as pd


class ErrorAnalyzer:
    """
    Menganalisis sampel kesalahan prediksi model (False Positive dan False Negative)
    untuk memahami kelemahan inferensi dan pola bias teks.
    """

    def analyze(
        self,
        df: pd.DataFrame,
        text_col: str,
        true_label_col: str,
        pred_label_col: str,
        prob_col: str,
        top_n: int = 10,
    ) -> Dict[str, Any]:
        """
        Mengekstraksi kasus False Positive (FP) dan False Negative (FN).

        Args:
            df (pd.DataFrame): Dataframe hasil inferensi.
            text_col (str): Kolom teks.
            true_label_col (str): Kolom label ground truth.
            pred_label_col (str): Kolom label prediksi.
            prob_col (str): Kolom skor probabilitas positif.
            top_n (int): Jumlah sampel teratas yang diekstraksi.

        Returns:
            Dict[str, Any]: Ringkasan error FP dan FN.
        """
        fp_df = df[(df[true_label_col] == 0) & (df[pred_label_col] == 1)]
        fn_df = df[(df[true_label_col] == 1) & (df[pred_label_col] == 0)]

        fp_samples = (
            fp_df.sort_values(by=prob_col, ascending=False)
            .head(top_n)[[text_col, true_label_col, pred_label_col, prob_col]]
            .to_dict(orient="records")
        )

        fn_samples = (
            fn_df.sort_values(by=prob_col, ascending=True)
            .head(top_n)[[text_col, true_label_col, pred_label_col, prob_col]]
            .to_dict(orient="records")
        )

        return {
            "total_samples": len(df),
            "false_positives_count": len(fp_df),
            "false_negatives_count": len(fn_df),
            "top_false_positives": fp_samples,
            "top_false_negatives": fn_samples,
        }

    def save_analysis(self, analysis_result: Dict[str, Any], path: str) -> None:
        """
        Menyimpan hasil analisis error ke file JSON.

        Args:
            analysis_result (Dict[str, Any]): Hasil dictionary analisis error.
            path (str): File tujuan output JSON.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=2)
