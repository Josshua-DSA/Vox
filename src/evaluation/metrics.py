import json
import os
from typing import Any, Dict
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


class MetricCalculator:
    """
    Menghitung metrik performa klasifikasi teks standar: Macro-F1, Precision, Recall, Accuracy, dan per-class metrics.
    """

    def compute_all(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ) -> Dict[str, Any]:
        """
        Menghitung seluruh metrik evaluasi klasifikasi biner.

        Args:
            y_true (np.ndarray): Label ground truth (0/1).
            y_pred (np.ndarray): Prediksi model (0/1).

        Returns:
            Dict[str, Any]: Ringkasan nilai metrik lengkap.
        """
        macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
        precision_macro = float(
            precision_score(y_true, y_pred, average="macro", zero_division=0)
        )
        recall_macro = float(
            recall_score(y_true, y_pred, average="macro", zero_division=0)
        )
        acc = float(accuracy_score(y_true, y_pred))

        report_dict = classification_report(
            y_true, y_pred, output_dict=True, zero_division=0
        )
        cm = confusion_matrix(y_true, y_pred).tolist()

        return {
            "macro_f1": macro_f1,
            "precision_macro": precision_macro,
            "recall_macro": recall_macro,
            "accuracy": acc,
            "per_class": {
                "non_toxic": {
                    "precision": float(report_dict.get("0", {}).get("precision", 0.0)),
                    "recall": float(report_dict.get("0", {}).get("recall", 0.0)),
                    "f1": float(report_dict.get("0", {}).get("f1-score", 0.0)),
                },
                "toxic": {
                    "precision": float(report_dict.get("1", {}).get("precision", 0.0)),
                    "recall": float(report_dict.get("1", {}).get("recall", 0.0)),
                    "f1": float(report_dict.get("1", {}).get("f1-score", 0.0)),
                },
            },
            "confusion_matrix": cm,
        }

    def save_metrics(self, metrics: Dict[str, Any], path: str) -> None:
        """
        Menyimpan hasil perhitungan metrik ke format file JSON.

        Args:
            metrics (Dict[str, Any]): Dictionary metrik.
            path (str): Lokasi file output JSON.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
