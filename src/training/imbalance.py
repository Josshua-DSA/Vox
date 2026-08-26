from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
from sklearn.utils.class_weight import compute_class_weight


class ImbalanceHandler:
    """
    Menyediakan mekanisme penanganan ketidakseimbangan kelas (class imbalance)
    melalui class weights, focal loss, atau teknik oversampling.

    Attributes:
        strategy (str): Opsi strategi ("none", "class_weight", "focal_loss", "oversample").
    """

    def __init__(self, strategy: str = "class_weight") -> None:
        """Inisialisasi strategi penanganan imbalance."""
        self.strategy = strategy

    def get_class_weights(self, y_train: np.ndarray) -> Optional[Dict[int, float]]:
        """
        Menghitung bobot invers frekuensi kelas untuk loss function.

        Args:
            y_train (np.ndarray): Label target training.

        Returns:
            Optional[Dict[int, float]]: Mapping bobot kelas {0: w0, 1: w1} atau None.
        """
        if self.strategy != "class_weight":
            return None

        classes = np.unique(y_train)
        weights = compute_class_weight(
            class_weight="balanced", classes=classes, y=y_train
        )
        return {int(c): float(w) for c, w in zip(classes, weights)}

    def oversample_minority(
        self, df: pd.DataFrame, label_col: str = "label", seed: int = 42
    ) -> pd.DataFrame:
        """
        Melakukan random oversampling pada kelas minoritas hingga seimbang.

        Args:
            df (pd.DataFrame): Dataframe input.
            label_col (str): Kolom target.
            seed (int): Random seed.

        Returns:
            pd.DataFrame: Dataframe yang telah diseimbangkan.
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
