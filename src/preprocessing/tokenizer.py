import pickle
from typing import Dict, List, Optional


class TextTokenizer:
    """
    Tokenizer teks berbasis frekuensi kata dengan representasi sequence integer.

    Attributes:
        vocab_size (int): Batas ukuran vocabulary.
        oov_token (str): Token penanda kata out-of-vocabulary.
        pad_token (str): Token penanda padding.
    """

    def __init__(
        self,
        vocab_size: int = 20000,
        oov_token: str = "<OOV>",
        pad_token: str = "<PAD>",
    ) -> None:
        """Inisialisasi parameter tokenizer."""
        self.vocab_size = vocab_size
        self.oov_token = oov_token
        self.pad_token = pad_token
        self.word_index: Dict[str, int] = {self.pad_token: 0, self.oov_token: 1}
        self.index_word: Dict[int, str] = {0: self.pad_token, 1: self.oov_token}
        self.is_fitted: bool = False

    def fit(self, texts: List[str]) -> None:
        """
        Membangun kamus vocabulary dari kumpulan teks korpus training.

        Args:
            texts (List[str]): List dokumen teks training.
        """
        word_freq: Dict[str, int] = {}
        for text in texts:
            tokens = text.split()
            for token in tokens:
                word_freq[token] = word_freq.get(token, 0) + 1

        sorted_words = sorted(
            word_freq.items(), key=lambda x: x[1], reverse=True
        )
        current_idx = 2
        for word, _ in sorted_words:
            if current_idx >= self.vocab_size:
                break
            self.word_index[word] = current_idx
            self.index_word[current_idx] = word
            current_idx += 1

        self.is_fitted = True

    def texts_to_sequences(self, texts: List[str]) -> List[List[int]]:
        """
        Mengonversi list teks menjadi list sequence integer token ID.

        Args:
            texts (List[str]): List string teks.

        Returns:
            List[List[int]]: List representasi integer token ID.
        """
        oov_idx = self.word_index[self.oov_token]
        sequences = []
        for text in texts:
            seq = [
                self.word_index.get(word, oov_idx) for word in text.split()
            ]
            sequences.append(seq)
        return sequences

    def save(self, path: str) -> None:
        """
        Menyimpan state objek tokenizer ke file disk.

        Args:
            path (str): Lokasi path file .pkl output.
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str) -> "TextTokenizer":
        """
        Memuat state objek tokenizer dari file disk.

        Args:
            path (str): Lokasi path file .pkl tokenizer.

        Returns:
            TextTokenizer: Instance tokenizer yang siap digunakan.
        """
        with open(path, "rb") as f:
            return pickle.load(f)
