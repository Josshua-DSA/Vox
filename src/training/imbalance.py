"""
ImbalanceHandler: penanganan ketidakseimbangan kelas via class weights,
Effective Number weighting, Binary Focal Loss, dan oversampling.
Sesuai ARCHITECTURE.md §4.4 dan PRD.md §3.3.
"""

from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd
from sklearn.utils.class_weight import compute_class_weight


class ImbalanceHandler:
    """
    Menyediakan mekanisme penanganan ketidakseimbangan kelas (class imbalance)
    melalui class weights, focal loss, atau teknik oversampling.

    Attributes:
        strategy: Opsi strategi ("none", "class_weight", "focal_loss", "oversample").
        gamma: Parameter pemfokusan Focal Loss (default 2.0).
        alpha: Parameter bobot kelas positif Focal Loss (default 0.25).
    """

    def __init__(
        self,
        strategy: str = "focal_loss",
        gamma: float = 2.0,
        alpha: float = 0.25,
    ) -> None:
        """
        Inisialisasi strategi penanganan imbalance.

        Args:
            strategy: Strategi yang digunakan.
            gamma: Parameter Focal Loss gamma.
            alpha: Parameter Focal Loss alpha.
        """
        self.strategy = strategy
        self.gamma = gamma
        self.alpha = alpha

    def get_class_weights(self, y_train: np.ndarray) -> dict[int, float] | None:
        """
        Menghitung bobot invers frekuensi kelas untuk loss function.

        Args:
            y_train: Label target training.

        Returns:
            Mapping bobot kelas {0: w0, 1: w1} atau None.
        """
        if self.strategy != "class_weight":
            return None

        classes = np.unique(y_train)
        weights = compute_class_weight(
            class_weight="balanced", classes=classes, y=y_train
        )
        return {int(c): float(w) for c, w in zip(classes, weights)}

    def compute_effective_num_weights(
        self, y_train: np.ndarray, beta: float = 0.999
    ) -> dict[int, float]:
        """
        Menghitung bobot kelas berdasarkan Effective Number of Samples (Cui et al., 2019).
        w_c = (1 - beta) / (1 - beta^n_c)

        Args:
            y_train: Label target training.
            beta: Parameter effective number (default 0.999).

        Returns:
            Mapping bobot kelas {0: w0, 1: w1}.
        """
        classes, counts = np.unique(y_train, return_counts=True)
        weights = {}
        for cls, n_c in zip(classes, counts):
            effective = (1.0 - beta) / (1.0 - beta**n_c)
            weights[int(cls)] = float(effective)

        # Normalisasi agar rata-rata bobot = 1.0
        total = sum(weights.values())
        n_classes = len(weights)
        for cls in weights:
            weights[cls] = weights[cls] * n_classes / total

        return weights

    def get_binary_focal_loss(self) -> Callable | None:
        """
        Mengembalikan fungsi Binary Focal Loss (Lin et al., 2017).
        L_FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t)

        Returns:
            Callable Keras-compatible loss function, atau None jika strategi bukan focal_loss.
        """
        if self.strategy != "focal_loss":
            return None

        gamma = self.gamma
        alpha = self.alpha

        def focal_loss(y_true: Any, y_pred: Any) -> Any:
            import tensorflow as tf

            y_true = tf.cast(y_true, tf.float32)
            y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)

            # p_t
            p_t = y_true * y_pred + (1.0 - y_true) * (1.0 - y_pred)

            # alpha_t
            alpha_t = y_true * alpha + (1.0 - y_true) * (1.0 - alpha)

            # focal weight
            focal_weight = alpha_t * tf.pow(1.0 - p_t, gamma)

            # cross entropy
            ce = -(y_true * tf.math.log(y_pred) + (1.0 - y_true) * tf.math.log(1.0 - y_pred))

            return tf.reduce_mean(focal_weight * ce)

        focal_loss.__name__ = "binary_focal_loss"
        return focal_loss

    def oversample_minority(
        self, df: pd.DataFrame, label_col: str = "label", seed: int = 42
    ) -> pd.DataFrame:
        """
        Melakukan random oversampling pada kelas minoritas hingga seimbang.

        Args:
            df: Dataframe input.
            label_col: Kolom target.
            seed: Random seed.

        Returns:
            Dataframe yang telah diseimbangkan.
        """
        counts = df[label_col].value_counts()
        max_count = counts.max()
        balanced_dfs = []
        for cls_val in counts.index:
            subset = df[df[label_col] == cls_val]
            if len(subset) < max_count:
                subset = subset.sample(
                    max_count, replace=True, random_state=seed
                )
            balanced_dfs.append(subset)
        return (
            pd.concat(balanced_dfs, axis=0)
            .sample(frac=1.0, random_state=seed)
            .reset_index(drop=True)
        )
