import json
import os
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


class MetricCalculator:
    """
    Menghitung metrik performa klasifikasi teks standar: Macro-F1, Precision, Recall, Accuracy, AUC-ROC, dan per-class metrics.
    """

    def compute_all(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: np.ndarray | None = None,
    ) -> dict[str, Any]:
        """
        Menghitung seluruh metrik evaluasi klasifikasi biner.

        Args:
            y_true (np.ndarray): Label ground truth (0/1).
            y_pred (np.ndarray): Prediksi model (0/1).
            y_prob (np.ndarray | None): Probabilitas prediksi kelas positif (0..1).

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

        auc_roc = None
        if y_prob is not None:
            try:
                auc_roc = float(roc_auc_score(y_true, y_prob))
            except Exception:
                auc_roc = 0.0

        report_dict = classification_report(
            y_true, y_pred, output_dict=True, zero_division=0
        )
        cm = confusion_matrix(y_true, y_pred).tolist()

        result = {
            "macro_f1": macro_f1,
            "precision_macro": precision_macro,
            "recall_macro": recall_macro,
            "accuracy": acc,
            "auc_roc": auc_roc,
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
        return result

    def save_metrics(self, metrics: dict[str, Any], path: str) -> None:
        """
        Menyimpan hasil perhitungan metrik ke format file JSON.

        Args:
            metrics (Dict[str, Any]): Dictionary metrik.
            path (str): Lokasi file output JSON.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

    def compute_by_group(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        groups: Any,
        min_samples: int = 1,
    ) -> dict[str, dict[str, Any]]:
        """Compute the binary metrics separately for each evaluation subgroup."""
        if min_samples < 1:
            raise ValueError("min_samples must be at least 1")
        group_values = np.asarray(groups)
        if len(y_true) != len(y_pred) or len(y_true) != len(group_values):
            raise ValueError("y_true, y_pred, and groups must have equal lengths")
        result: dict[str, dict[str, Any]] = {}
        for group in dict.fromkeys(group_values.tolist()):
            mask = group_values == group
            if int(mask.sum()) < min_samples:
                continue
            result[str(group)] = self.compute_all(y_true[mask], y_pred[mask])
        return result

    def compute_multilabel(
        self, y_true: np.ndarray, y_pred: np.ndarray
    ) -> dict[str, Any]:
        """Compute per-label and macro/micro metrics for binary multilabel data."""
        true = np.asarray(y_true)
        pred = np.asarray(y_pred)
        if true.ndim != 2 or pred.shape != true.shape:
            raise ValueError("multilabel arrays must be 2D with equal shapes")
        labels = []
        for index in range(true.shape[1]):
            labels.append(
                {
                    "precision": float(
                        precision_score(true[:, index], pred[:, index], zero_division=0)
                    ),
                    "recall": float(
                        recall_score(true[:, index], pred[:, index], zero_division=0)
                    ),
                    "f1": float(
                        f1_score(true[:, index], pred[:, index], zero_division=0)
                    ),
                }
            )
        return {
            "macro_f1": float(f1_score(true, pred, average="macro", zero_division=0)),
            "micro_f1": float(f1_score(true, pred, average="micro", zero_division=0)),
            "per_label": labels,
        }
