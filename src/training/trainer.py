from typing import Any, Dict, Optional
import numpy as np
from src.models.base_model import BaseModel
from src.training.imbalance import ImbalanceHandler
from src.utils.logger import Logger


class ModelTrainer:
    """
    Mengorkestrasikan proses fitting model, validasi, dan callback evaluasi.

    Attributes:
        model (BaseModel): Objek model yang akan dilatih.
        imbalance_handler (ImbalanceHandler): Pengelola bobot/penyeimbang kelas.
    """

    def __init__(
        self,
        model: BaseModel,
        imbalance_handler: Optional[ImbalanceHandler] = None,
    ) -> None:
        """Inisialisasi ModelTrainer."""
        self.model = model
        self.imbalance_handler = (
            imbalance_handler if imbalance_handler else ImbalanceHandler("none")
        )
        self.logger = Logger.get_logger("ModelTrainer")

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Menjalankan training pipeline lengkap.

        Args:
            X_train (np.ndarray): Padded sequence token train.
            y_train (np.ndarray): Label target train.
            X_val (np.ndarray): Padded sequence token val.
            y_val (np.ndarray): Label target val.

        Returns:
            Dict[str, Any]: Log riwayat metrik training per epoch.
        """
        self.logger.info("Memulai proses fitting model...")
        class_weights = self.imbalance_handler.get_class_weights(y_train)
        if class_weights:
            self.logger.info(f"Class weight diaktifkan: {class_weights}")

        history = self.model.train(
            X_train=X_train,
            y_train=y_train,
            X_val=X_val,
            y_val=y_val,
            class_weight=class_weights,
        )
        self.logger.info("Training selesai.")
        return history
