"""
AnnotatorAgreementAggregator: agregasi label multi-annotator via majority voting
dan perhitungan Fleiss' Kappa sesuai ARCHITECTURE.md §1.1.
"""

import ast

import numpy as np
import pandas as pd


class AnnotatorAgreementAggregator:
    """
    Mengagregasi daftar label multi-anotator per baris menggunakan aturan
    majority voting serta menghitung skor kesepakatan anotasi.

    Attributes:
        threshold: Rasio minimum vote positif untuk label 1 (default 0.5).
    """

    def __init__(self, threshold: float = 0.5) -> None:
        """
        Inisialisasi aggregator.

        Args:
            threshold: Batas rasio vote untuk konsensus label positif.
        """
        if not 0.0 < threshold <= 1.0:
            raise ValueError(f"threshold harus dalam (0.0, 1.0], dapat: {threshold}")
        self.threshold = threshold

    @staticmethod
    def _parse_votes(raw: str | list) -> list[int]:
        """
        Parse string representasi list vote menjadi list integer.

        Args:
            raw: String seperti "['0', '1', '1']" atau list yang sudah parsed.

        Returns:
            List integer vote (0 atau 1).
        """
        if isinstance(raw, list):
            return [int(v) for v in raw]
        if isinstance(raw, str):
            try:
                parsed = ast.literal_eval(raw)
                return [int(v) for v in parsed]
            except (ValueError, SyntaxError):
                return []
        return []

    def aggregate_votes(self, votes_list: list[int]) -> tuple[int, float]:
        """
        Mengembalikan label konsensus dan skor agreement.

        Args:
            votes_list: List integer vote (0/1).

        Returns:
            Tuple (label_biner, agreement_ratio).
            - label_biner: 1 jika rasio vote positif >= threshold, 0 selain itu.
            - agreement_ratio: max(positif, negatif) / total ∈ [0.5, 1.0].
        """
        if not votes_list:
            return 0, 0.0
        total = len(votes_list)
        positives = sum(votes_list)
        ratio = positives / total
        label = 1 if ratio >= self.threshold else 0
        agreement = max(positives, total - positives) / total
        return label, round(agreement, 4)

    def compute_dataset_kappa(self, df_raw: pd.DataFrame, col: str = "toxicity") -> float:
        """
        Menghitung Fleiss' Kappa untuk seluruh dataset pada kolom tertentu.

        Args:
            df_raw: DataFrame mentah dengan kolom vote multi-anotator.
            col: Nama kolom vote (default "toxicity").

        Returns:
            Skor Fleiss' Kappa.
        """
        votes_matrix = df_raw[col].apply(self._parse_votes).tolist()
        if not votes_matrix:
            return 0.0

        # Bangun tabel kategori per item: [count_0, count_1]
        n_items = len(votes_matrix)
        category_counts = np.zeros((n_items, 2), dtype=np.float64)
        for i, votes in enumerate(votes_matrix):
            for v in votes:
                if v in (0, 1):
                    category_counts[i, v] += 1

        n_raters_per_item = category_counts.sum(axis=1)
        # Filter baris dengan >= 2 rater
        valid = n_raters_per_item >= 2
        if valid.sum() == 0:
            return 0.0

        category_counts = category_counts[valid]
        n_raters_per_item = n_raters_per_item[valid]
        n_items_valid = int(valid.sum())

        # P_i: proporsi agreement per item
        p_i = np.zeros(n_items_valid)
        for i in range(n_items_valid):
            n = n_raters_per_item[i]
            if n <= 1:
                p_i[i] = 1.0
            else:
                p_i[i] = (np.sum(category_counts[i] ** 2) - n) / (n * (n - 1))

        p_bar = np.mean(p_i)

        # P_j: proporsi assignment per kategori
        total_ratings = category_counts.sum()
        p_j = category_counts.sum(axis=0) / total_ratings
        p_e = np.sum(p_j**2)

        if abs(1.0 - p_e) < 1e-10:
            return 1.0 if abs(p_bar - 1.0) < 1e-10 else 0.0

        kappa = (p_bar - p_e) / (1.0 - p_e)
        return round(float(kappa), 4)

    def process_dataframe(
        self,
        df_raw: pd.DataFrame,
        vote_col: str = "toxicity",
        label_col: str = "label",
        agreement_col: str = "annotator_agreement",
    ) -> pd.DataFrame:
        """
        Menambahkan kolom label konsensus dan skor agreement ke DataFrame.

        Args:
            df_raw: DataFrame mentah.
            vote_col: Kolom berisi string list vote.
            label_col: Nama kolom output label biner.
            agreement_col: Nama kolom output skor agreement.

        Returns:
            DataFrame dengan kolom baru label dan agreement.
        """
        df = df_raw.copy()
        votes = df[vote_col].apply(self._parse_votes)
        results = votes.apply(self.aggregate_votes)
        df[label_col] = results.apply(lambda x: x[0])
        df[agreement_col] = results.apply(lambda x: x[1])
        return df
