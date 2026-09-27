"""
ModelTrainer: orkestrator training dual-input CNN dengan dukungan focal loss.
"""

from typing import Any

import numpy as np

from src.models.base_model import BaseModel
from src.training.imbalance import ImbalanceHandler
from src.utils.logger import Logger


class ModelTrainer:
    """
    Mengorkestrasikan proses fitting model dual-input, validasi, dan callback.

    Attributes:
        model: Objek model yang akan dilatih.
        imbalance_handler: Pengelola bobot/penyeimbang kelas.
    """

    def __init__(
        self,
        model: BaseModel,
        imbalance_handler: ImbalanceHandler | None = None,
    ) -> None:
        """Inisialisasi ModelTrainer."""
        self.model = model
        self.imbalance_handler = (
            imbalance_handler if imbalance_handler else ImbalanceHandler("none")
        )
        self.logger = Logger.get_logger("ModelTrainer")

    def fit(
        self,
        X_text_train: np.ndarray,
        X_topic_train: np.ndarray,
        y_train: np.ndarray,
        X_text_val: np.ndarray,
        X_topic_val: np.ndarray,
        y_val: np.ndarray,
    ) -> dict[str, Any]:
        """
        Menjalankan training pipeline lengkap dual-input.

        Args:
            X_text_train: Padded sequence token train.
            X_topic_train: Integer ID topik train.
            y_train: Label target train.
            X_text_val: Padded sequence token val.
            X_topic_val: Integer ID topik val.
            y_val: Label target val.

        Returns:
            Log riwayat metrik training per epoch.
        """
        self.logger.info("Memulai proses fitting model...")

        class_weights = self.imbalance_handler.get_class_weights(y_train)
        loss_fn = self.imbalance_handler.get_binary_focal_loss()

        if loss_fn is not None:
            self.logger.info(
                f"Focal Loss diaktifkan (gamma={self.imbalance_handler.gamma}, "
                f"alpha={self.imbalance_handler.alpha})"
            )
        elif class_weights:
            self.logger.info(f"Class weight diaktifkan: {class_weights}")

        history = self.model.train(
            X_text_train=X_text_train,
            X_topic_train=X_topic_train,
            y_train=y_train,
            X_text_val=X_text_val,
            X_topic_val=X_topic_val,
            y_val=y_val,
            class_weight=class_weights,
            loss_fn=loss_fn,
        )
        self.logger.info("Training selesai.")
        return history
