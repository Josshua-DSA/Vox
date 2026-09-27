from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class BaseModel(ABC):
    """
    Abstract Base Class untuk arsitektur model klasifikasi teks.
    Mendukung dual-input (teks + topic) sesuai Context-Aware architecture.
    """

    def __init__(self, config: Any) -> None:
        """
        Inisialisasi BaseModel dengan objek konfigurasi.

        Args:
            config: Objek Config yang memuat hyperparameter model.
        """
        self.config = config
        self.model: Any = None

    @abstractmethod
    def build_model(
        self, embedding_matrix: np.ndarray | None = None
    ) -> Any:
        """
        Membangun dan mengompilasi graf arsitektur neural network model.

        Args:
            embedding_matrix: Bobot pre-trained embedding (opsional).

        Returns:
            Instance objek model terkompilasi.
        """

    @abstractmethod
    def train(
        self,
        X_text_train: np.ndarray,
        X_topic_train: np.ndarray,
        y_train: np.ndarray,
        X_text_val: np.ndarray,
        X_topic_val: np.ndarray,
        y_val: np.ndarray,
        class_weight: dict[int, float] | None = None,
        loss_fn: Any | None = None,
    ) -> dict[str, Any]:
        """
        Melatih model dual-input dan mengembalikan history performa epoch.

        Args:
            X_text_train: Padded sequence token train.
            X_topic_train: Integer ID topik train.
            y_train: Label train.
            X_text_val: Padded sequence token val.
            X_topic_val: Integer ID topik val.
            y_val: Label val.
            class_weight: Bobot penalti kelas.
            loss_fn: Custom loss function (misal Focal Loss).

        Returns:
            History loss dan metrik per epoch.
        """

    @abstractmethod
    def predict(
        self,
        X_text: np.ndarray,
        X_topic: np.ndarray,
        threshold: float = 0.5,
    ) -> np.ndarray:
        """
        Menghasilkan prediksi kelas biner (0 atau 1).

        Args:
            X_text: Matrix input sequence token.
            X_topic: Array integer ID topik.
            threshold: Batas ambang klasifikasi biner.

        Returns:
            Array prediksi label kelas biner.
        """

    @abstractmethod
    def predict_proba(
        self, X_text: np.ndarray, X_topic: np.ndarray
    ) -> np.ndarray:
        """
        Menghitung nilai estimasi probabilitas positif.

        Args:
            X_text: Matrix input sequence token.
            X_topic: Array integer ID topik.

        Returns:
            Array nilai probabilitas [0.0, 1.0].
        """

    @abstractmethod
    def save(self, path: str) -> None:
        """
        Menyimpan arsitektur dan bobot model ke file disk.

        Args:
            path: Lokasi penyimpanan file model.
        """

    @abstractmethod
    def load(self, path: str) -> None:
        """
        Memuat bobot model dari file disk.

        Args:
            path: Lokasi file model tersimpan.
        """
