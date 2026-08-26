from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import numpy as np


class BaseModel(ABC):
    """
    Abstract Base Class untuk arsitektur model klasifikasi teks.
    Semua implementasi model eksperimen wajib mewarisi class ini.
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
    def build_model(self) -> Any:
        """
        Membangun dan mengompilasi graf arsitektur neural network model.

        Returns:
            Any: Instance objek model terkompilasi.
        """
        pass

    @abstractmethod
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        class_weight: Optional[Dict[int, float]] = None,
    ) -> Dict[str, Any]:
        """
        Melatih model dan mengembalikan dictionary history performa epoch.

        Args:
            X_train (np.ndarray): Padded sequence token train.
            y_train (np.ndarray): Label train.
            X_val (np.ndarray): Padded sequence token val.
            y_val (np.ndarray): Label val.
            class_weight (Dict[int, float], optional): Bobot penalti kelas.

        Returns:
            Dict[str, Any]: History loss dan metrik per epoch.
        """
        pass

    @abstractmethod
    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """
        Menghasilkan diskrit prediksi kelas (0 atau 1).

        Args:
            X (np.ndarray): Matrix input sequence token.
            threshold (float): Batas ambang klasifikasi biner.

        Returns:
            np.ndarray: Array prediksi label kelas biner.
        """
        pass

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Menghitung nilai estimasi probabilitas positif kelas hate speech/toksik.

        Args:
            X (np.ndarray): Matrix input sequence token.

        Returns:
            np.ndarray: Array nilai probabilitas [0.0, 1.0].
        """
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """
        Menyimpan arsitektur dan bobot bobot model ke file disk.

        Args:
            path (str): Lokasi penyimpanan file model.
        """
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """
        Memuat bobot bobot model dari file disk.

        Args:
            path (str): Lokasi file model tersimpan.
        """
        pass
