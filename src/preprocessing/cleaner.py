import re
from typing import List


class TextCleaner:
    """
    Membersihkan teks media sosial berbahasa Indonesia sebelum proses tokenisasi.

    Attributes:
        remove_urls (bool): Hapus URL dari teks.
        remove_mentions (bool): Hapus @mention pengguna.
        remove_hashtags (bool): Hapus simbol hashtag (#).
        remove_punctuation (bool): Hapus tanda baca berlebih.
        lowercase (bool): Normalisasi ke huruf kecil.
    """

    def __init__(
        self,
        remove_urls: bool = True,
        remove_mentions: bool = True,
        remove_hashtags: bool = False,
        remove_punctuation: bool = True,
        lowercase: bool = True,
    ) -> None:
        """Inisialisasi konfigurasi aturan cleaning teks."""
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_punctuation = remove_punctuation
        self.lowercase = lowercase

    def clean(self, text: str) -> str:
        """
        Menjalankan seluruh pipeline pembersihan untuk satu string teks.

        Args:
            text (str): Teks mentah.

        Returns:
            str: Teks bersih.
        """
        if not isinstance(text, str):
            return ""

        if self.remove_urls:
            text = self._remove_url(text)
        if self.remove_mentions:
            text = self._remove_mention(text)
        if self.remove_hashtags:
            text = self._remove_hashtag(text)
        if self.lowercase:
            text = text.lower()
        if self.remove_punctuation:
            text = self._remove_punct(text)

        text = self._remove_extra_spaces(text)
        return text

    def clean_batch(self, texts: List[str]) -> List[str]:
        """
        Menerapkan fungsi clean() pada sekumpulan list teks.

        Args:
            texts (List[str]): List teks mentah.

        Returns:
            List[str]: List teks yang sudah dibersihkan.
        """
        return [self.clean(t) for t in texts]

    def _remove_url(self, text: str) -> str:
        return re.sub(r"https?://\S+|www\.\S+", "", text)

    def _remove_mention(self, text: str) -> str:
        return re.sub(r"@\w+", "", text)

    def _remove_hashtag(self, text: str) -> str:
        return re.sub(r"#\w+", "", text)

    def _remove_punct(self, text: str) -> str:
        return re.sub(r"[^\w\s]", " ", text)

    def _remove_extra_spaces(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()
