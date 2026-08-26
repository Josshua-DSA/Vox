import os
from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix


class ConfusionMatrixPlotter:
    """
    Visualisasi heatmap confusion matrix untuk evaluasi model klasifikasi.
    """

    def __init__(
        self, class_names: Optional[List[str]] = None
    ) -> None:
        """Inisialisasi nama kelas target."""
        self.class_names = (
            class_names if class_names else ["Non-toxic", "Toxic"]
        )

    def plot_and_save(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        output_path: str = "outputs/plots/confusion_matrix.png",
        title: str = "Confusion Matrix - Indonesian Hate Speech CNN",
    ) -> str:
        """
        Menghasilkan dan menyimpan gambar plot confusion matrix.

        Args:
            y_true (np.ndarray): Label sebenarnya.
            y_pred (np.ndarray): Label hasil prediksi.
            output_path (str): File tujuan penyimpanan gambar PNG.
            title (str): Judul grafik plot.

        Returns:
            str: Path file gambar tersimpan.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(6, 5))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=self.class_names,
            yticklabels=self.class_names,
        )
        plt.title(title)
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
        return output_path
