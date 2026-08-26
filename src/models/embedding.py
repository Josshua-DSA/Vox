import os
from typing import Dict
import numpy as np


class EmbeddingLoader:
    """
    Memuat dan menyusun matrix bobot embedding pre-trained (FastText / Word2Vec).

    Attributes:
        embedding_dim (int): Dimensi vektor kata.
    """

    def __init__(self, embedding_dim: int = 128) -> None:
        """Inisialisasi dimensi embedding."""
        self.embedding_dim = embedding_dim

    def load_pretrained_vectors(self, file_path: str) -> Dict[str, np.ndarray]:
        """
        Membaca file format teks word vector (.vec / .txt).

        Args:
            file_path (str): Path ke file pre-trained vectors.

        Returns:
            Dict[str, np.ndarray]: Mapping kata ke array embedding.
        """
        embeddings_index: Dict[str, np.ndarray] = {}
        if not os.path.exists(file_path):
            return embeddings_index

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                values = line.rstrip().split(" ")
                word = values[0]
                try:
                    coefs = np.asarray(values[1:], dtype="float32")
                    if len(coefs) == self.embedding_dim:
                        embeddings_index[word] = coefs
                except ValueError:
                    continue
        return embeddings_index

    def build_embedding_matrix(
        self,
        word_index: Dict[str, int],
        embeddings_index: Dict[str, np.ndarray],
        vocab_size: int,
    ) -> np.ndarray:
        """
        Membentuk matrix 2D berukuran (vocab_size, embedding_dim) untuk layer Embedding.

        Args:
            word_index (Dict[str, int]): Mapping kata ke token index.
            embeddings_index (Dict[str, np.ndarray]): Mapping kata ke vector.
            vocab_size (int): Ukuran vocabulary.

        Returns:
            np.ndarray: Embedding matrix.
        """
        embedding_matrix = np.zeros((vocab_size, self.embedding_dim), dtype=np.float32)
        for word, i in word_index.items():
            if i < vocab_size:
                vector = embeddings_index.get(word)
                if vector is not None:
                    embedding_matrix[i] = vector
        return embedding_matrix
