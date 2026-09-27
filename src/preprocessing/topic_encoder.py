"""
TopicEncoder: mapping kategorikal metadata topik ke integer ID dan multi-hot vector.
Mendukung 7 kategori kanonikal sesuai ARCHITECTURE.md §4.2.
"""

import json
import os
from typing import Any

import numpy as np
import pandas as pd


class TopicEncoder:
    """
    Mengelola mapping kategorikal untuk metadata topik (Politik, Agama, SARA, dll.)
    menjadi indeks integer atau vektor multi-hot representation.

    Attributes:
        canonical_topics: Daftar 7 topik kanonikal terurut.
        topic_to_id: Mapping string topik ke integer ID.
        id_to_topic: Mapping integer ID ke string topik.
        unknown_id: Integer ID untuk topik yang tidak dikenal.
    """

    def __init__(self, canonical_topics: list[str] | None = None) -> None:
        """
        Inisialisasi TopicEncoder.

        Args:
            canonical_topics: Daftar topik kanonikal. Default 7 topik dari Config.
        """
        if canonical_topics is None:
            canonical_topics = [
                "Politik",
                "Agama",
                "SARA",
                "Gender",
                "Pemilu2024",
                "Umum",
                "UNKNOWN",
            ]
        self.canonical_topics: list[str] = canonical_topics
        self.topic_to_id: dict[str, int] = {
            t: i for i, t in enumerate(self.canonical_topics)
        }
        self.id_to_topic: dict[int, str] = {
            i: t for t, i in self.topic_to_id.items()
        }
        self.unknown_id: int = self.topic_to_id.get("UNKNOWN", len(self.canonical_topics) - 1)

    def fit(self, topics_series: pd.Series) -> "TopicEncoder":
        """
        Fit encoder pada kolom topik. Topik di luar kanonikal di-map ke UNKNOWN.
        Operasi ini bersifat no-op karena mapping sudah fixed, tetapi disediakan
        agar konsisten dengan API fit/transform.

        Args:
            topics_series: Pandas Series berisi string topik.

        Returns:
            Self untuk chaining.
        """
        return self

    def transform_single(self, topic: str) -> int:
        """
        Mengonversi satu string topik ke integer ID.

        Args:
            topic: String nama topik.

        Returns:
            Integer ID topik. Topik tidak dikenal mendapat unknown_id.
        """
        if not isinstance(topic, str):
            return self.unknown_id
        return self.topic_to_id.get(topic, self.unknown_id)

    def transform(self, topics: pd.Series | list[str]) -> np.ndarray:
        """
        Mengonversi series/list topik ke array integer ID.

        Args:
            topics: Series atau list string topik.

        Returns:
            np.ndarray 1D berisi integer ID topik.
        """
        if isinstance(topics, pd.Series):
            topics = topics.tolist()
        return np.array([self.transform_single(t) for t in topics], dtype=np.int32)

    def transform_multi_hot(self, topic_list: list[str]) -> np.ndarray:
        """
        Mengonversi list topik menjadi vektor multi-hot (untuk teks multi-topik).

        Args:
            topic_list: List string topik.

        Returns:
            np.ndarray vektor multi-hot berukuran (num_topics,).
        """
        vec = np.zeros(len(self.canonical_topics), dtype=np.int32)
        for t in topic_list:
            idx = self.topic_to_id.get(t, self.unknown_id)
            vec[idx] = 1
        return vec

    def inverse_transform(self, topic_id: int) -> str:
        """
        Mengonversi integer ID kembali ke string topik.

        Args:
            topic_id: Integer ID topik.

        Returns:
            String nama topik.
        """
        return self.id_to_topic.get(topic_id, "UNKNOWN")

    def save(self, path: str) -> None:
        """
        Menyimpan mapping encoder ke file JSON.

        Args:
            path: Lokasi file output.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        payload: dict[str, Any] = {
            "canonical_topics": self.canonical_topics,
            "topic_to_id": self.topic_to_id,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> "TopicEncoder":
        """
        Memuat encoder dari file JSON.

        Args:
            path: Lokasi file JSON.

        Returns:
            Instance TopicEncoder.
        """
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return cls(canonical_topics=data["canonical_topics"])
