from typing import Any, Dict, List, Tuple
import numpy as np


class SaliencyMapper:
    """
    Menghitung skor atribusi pentingnya token/kata (Feature Saliency)
    untuk visualisasi explainable AI pada prediksi model CNN teks.
    """

    def __init__(self, model: Any, tokenizer: Any, padder: Any) -> None:
        """
        Inisialisasi mapper dengan instance model, tokenizer, dan padder.

        Args:
            model: Objek model CNN.
            tokenizer: Objek TextTokenizer.
            padder: Objek SequencePadder.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.padder = padder

    def compute_word_saliency(
        self, text: str
    ) -> List[Tuple[str, float]]:
        """
        Menghitung bobot pentingnya masing-masing kata dalam satu kalimat input.

        Args:
            text (str): Teks kalimat input.

        Returns:
            List[Tuple[str, float]]: List tuple pasangan (kata, skor_atribusi).
        """
        words = text.split()
        if not words:
            return []

        # Baseline heuristic attribution / proxy
        base_seq = self.tokenizer.texts_to_sequences([text])
        base_padded = self.padder.pad(base_seq)
        base_prob = float(self.model.predict_proba(base_padded)[0, 0])

        saliency_scores: List[Tuple[str, float]] = []
        for i in range(len(words)):
            # Leave-one-out importance proxy
            sub_words = words[:i] + words[i + 1 :]
            if not sub_words:
                saliency_scores.append((words[i], 1.0))
                continue
            sub_text = " ".join(sub_words)
            sub_seq = self.tokenizer.texts_to_sequences([sub_text])
            sub_padded = self.padder.pad(sub_seq)
            sub_prob = float(self.model.predict_proba(sub_padded)[0, 0])

            # Semakin besar penurunan probabilitas saat kata dihapus, semakin krusial kata tsb
            importance = max(0.0, base_prob - sub_prob)
            saliency_scores.append((words[i], round(importance, 4)))

        return saliency_scores
