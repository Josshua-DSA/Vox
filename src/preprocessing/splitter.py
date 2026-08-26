import os
from typing import Dict, Tuple
import pandas as pd
from sklearn.model_selection import train_test_split


class DataSplitter:
    """
    Membagi dataset secara terstratifikasi ke dalam subset train, validation, dan test.

    Attributes:
        train_ratio (float): Proporsi data latih.
        val_ratio (float): Proporsi data validasi.
        test_ratio (float): Proporsi data uji.
        seed (int): Random seed untuk reprodusibilitas.
    """

    def __init__(
        self,
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: int = 42,
    ) -> None:
        """Inisialisasi rasio split dan seed."""
        if not abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5:
            raise ValueError("Total rasio split harus bernilai 1.0")
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

    def split(
        self, df: pd.DataFrame, stratify_col: str = "label"
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Membagi DataFrame menjadi train, val, dan test set.

        Args:
            df (pd.DataFrame): DataFrame input.
            stratify_col (str): Nama kolom target untuk stratified sampling.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: (train_df, val_df, test_df)
        """
        temp_val_test_ratio = self.val_ratio + self.test_ratio
        train_df, temp_df = train_test_split(
            df,
            test_size=temp_val_test_ratio,
            random_state=self.seed,
            stratify=df[stratify_col] if stratify_col in df else None,
        )

        relative_test_ratio = self.test_ratio / temp_val_test_ratio
        val_df, test_df = train_test_split(
            temp_df,
            test_size=relative_test_ratio,
            random_state=self.seed,
            stratify=temp_df[stratify_col] if stratify_col in temp_df else None,
        )

        return (
            train_df.reset_index(drop=True),
            val_df.reset_index(drop=True),
            test_df.reset_index(drop=True),
        )

    def save_splits(
        self,
        train_df: pd.DataFrame,
        val_df: pd.DataFrame,
        test_df: pd.DataFrame,
        output_dir: str = "data/splits/",
    ) -> Dict[str, str]:
        """
        Menyimpan hasil partisi dataset ke format file CSV.

        Args:
            train_df (pd.DataFrame): Data train.
            val_df (pd.DataFrame): Data validasi.
            test_df (pd.DataFrame): Data uji.
            output_dir (str): Folder direktori tujuan.

        Returns:
            Dict[str, str]: Path masing-masing file split yang tersimpan.
        """
        os.makedirs(output_dir, exist_ok=True)
        paths = {
            "train": os.path.join(output_dir, "train.csv"),
            "val": os.path.join(output_dir, "val.csv"),
            "test": os.path.join(output_dir, "test.csv"),
        }
        train_df.to_csv(paths["train"], index=False)
        val_df.to_csv(paths["val"], index=False)
        test_df.to_csv(paths["test"], index=False)
        return paths
