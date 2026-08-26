from typing import List
import numpy as np


class SequencePadder:
    """
    Menyelaraskan panjang urutan sequence token ID ke dimensi tetap (max_len).

    Attributes:
        max_len (int): Panjang maksimum sequence.
        padding (str): Posisi padding ('post' atau 'pre').
        truncating (str): Posisi pemangkasan ('post' atau 'pre').
        pad_value (int): Nilai integer untuk padding token.
    """

    def __init__(
        self,
        max_len: int = 128,
        padding: str = "post",
        truncating: str = "post",
        pad_value: int = 0,
    ) -> None:
        """Inisialisasi konfigurasi panjang dan strategi padding."""
        self.max_len = max_len
        self.padding = padding
        self.truncating = truncating
        self.pad_value = pad_value

    def pad(self, sequences: List[List[int]]) -> np.ndarray:
        """
        Melakukan padding atau truncating pada batch sequences.

        Args:
            sequences (List[List[int]]): List sequence ID dengan panjang bervariasi.

        Returns:
            np.ndarray: Matrix 2D dengan dimensi (num_samples, max_len).
        """
        num_samples = len(sequences)
        padded_matrix = np.full(
            (num_samples, self.max_len), self.pad_value, dtype=np.int32
        )

        for i, seq in enumerate(sequences):
            if not seq:
                continue

            # Truncating
            if len(seq) > self.max_len:
                if self.truncating == "post":
                    trunc_seq = seq[: self.max_len]
                else:
                    trunc_seq = seq[-self.max_len :]
            else:
                trunc_seq = seq

            # Padding
            seq_len = len(trunc_seq)
            if self.padding == "post":
                padded_matrix[i, :seq_len] = trunc_seq
            else:
                padded_matrix[i, -seq_len:] = trunc_seq

        return padded_matrix
