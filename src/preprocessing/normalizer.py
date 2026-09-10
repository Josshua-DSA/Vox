"""
Normalisasi prapemrosesan teks media sosial berbahasa Indonesia.

Menormalkan leet-speak, pengulangan karakter, slang, dan emoji menjadi
bentuk kata baku sebelum proses pembersihan dan tokenisasi.
"""

import json
import re

from src.utils.config import Config
from src.utils.logger import Logger


class SlangNormalizer:
    """
    Menormalkan kata-kata gaul, slang, singkatan, penyamaran karakter
    (leet-speak), dan emoji pada teks media sosial bahasa Indonesia.

    Pipeline normalisasi berurutan: decode leet -> collapse repeats ->
    expand emoji -> expand slang.

    Attributes:
        slang_dict (Dict[str, str]): Peta slang/singkatan ke bentuk baku.
        emoji_map (Dict[str, str]): Peta emoji/smiley ASCII ke kata sentimen.
        leet_map (Dict[str, str]): Peta karakter leet-speak ke huruf.
    """

    LEET_MAP: dict[str, str] = {
        "4": "a", "@": "a", "8": "b", "(": "c", "3": "e", "9": "g",
        "#": "h", "1": "i", "!": "i", "|": "i", "0": "o", "5": "s",
        "$": "s", "7": "t", "v": "u", "%": "x",
    }

    _REPEAT_PATTERN = re.compile(r"(.)\1{2,}")

    def __init__(
        self,
        slang_dict: dict[str, str] | None = None,
        emoji_map: dict[str, str] | None = None,
        config: Config | None = None,
    ) -> None:
        """
        Inisialisasi normalizer dengan leksikon slang, emoji, dan leet map.

        Args:
            slang_dict (Optional[Dict[str, str]]): Kamus kustom slang.
                Jika None, dimuat dari Config.SLANG_DICT_PATH.
            emoji_map (Optional[Dict[str, str]]): Kamus kustom emoji.
                Jika None, dimuat dari Config.EMOJI_MAP_PATH.
            config (Optional[Config]): Instance konfigurasi terpusat.

        Raises:
            FileNotFoundError: File resource leksikon tidak ditemukan saat
                tidak disediakan lewat argumen.
        """
        self.config = config or Config()
        self.logger = Logger.get_logger("SlangNormalizer")
        self.slang_dict: dict[str, str] = slang_dict if slang_dict is not None \
            else self._load_json(self.config.SLANG_DICT_PATH)
        self.emoji_map: dict[str, str] = emoji_map if emoji_map is not None \
            else self._load_json(self.config.EMOJI_MAP_PATH)
        self.leet_map = dict(self.LEET_MAP)
        self.logger.info(
            f"Leksikon termuat: {len(self.slang_dict)} slang, "
            f"{len(self.emoji_map)} emoji."
        )

    @staticmethod
    def _load_json(path: str) -> dict[str, str]:
        """
        Membaca berkas JSON leksikon.

        Args:
            path (str): Lokasi file JSON.

        Returns:
            Dict[str, str]: Isi leksikon.
        """
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def decode_leet(self, text: str) -> str:
        """
        Mengonversi karakter leet-speak pada token alphabetic.

        Konversi hanya berlaku pada token yang mengandung minimal satu digit
        di antara huruf (misal: '4nj1ng' -> 'anjing', 'k0nt0l' -> 'kontol'),
        sehingga angka legitimate seperti '2024' atau 'rp 75' tidak rusak.

        Args:
            text (str): Teks masukan.

        Returns:
            str: Teks dengan leet-speak terdekode.
        """
        tokens = re.split(r"(\s+)", text.lower())
        decoded = []
        for tok in tokens:
            if re.search(r"[a-z]", tok) and re.search(r"\d", tok):
                tok = "".join(self.leet_map.get(ch, ch) for ch in tok)
            decoded.append(tok)
        return "".join(decoded)

    def collapse_repeating_chars(self, text: str) -> str:
        """
        Mereduksi pengulangan karakter lebih dari dua kali menjadi maksimal
        dua (batas konservatif agar bentuk doubled seperti 'baa' tidak rusak).

        Contoh: 'begooolll' -> 'begooll', 'anjinggg' -> 'anjing'.

        Args:
            text (str): Teks masukan.

        Returns:
            str: Teks dengan pengulangan karakter dikurangi maksimal 2.
        """
        return self._REPEAT_PATTERN.sub(r"\1\1", text)

    def expand_emoji(self, text: str) -> str:
        """
        Mengubah emoji dan smiley ASCII menjadi kata sentimen pendamping.

        Emoji tidak dibuang, melainkan diganti padanan katanya sehingga sinyal
        emosional tetap dapat dipelajari model (mis. '😂' -> 'tertawa').

        Args:
            text (str): Teks masukan.

        Returns:
            str: Teks dengan emoji tergantikan kata.
        """
        for token, repl in self.emoji_map.items():
            if token in text:
                text = text.replace(token, f" {repl} ")
        return text

    def expand_slang(self, text: str) -> str:
        """
        Memetakan singkatan dan kata slang ke bentuk standar leksikon.

        Args:
            text (str): Teks masukan.

        Returns:
            str: Teks dengan slang terpetakan.
        """
        tokens = re.split(r"(\s+)", text)
        mapped = [self.slang_dict.get(tok, tok) for tok in tokens]
        return "".join(mapped)

    def normalize(self, text: str) -> str:
        """
        Menjalankan pipeline normalisasi penuh secara berurutan.

        Args:
            text (str): Teks mentah.

        Returns:
            str: Teks ternormalisasi.
        """
        if not isinstance(text, str) or not text:
            return ""
        text = self.decode_leet(text)
        text = self.collapse_repeating_chars(text)
        text = self.expand_emoji(text)
        text = self.expand_slang(text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
