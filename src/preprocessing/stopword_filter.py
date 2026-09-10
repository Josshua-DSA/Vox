"""
Filter stopword aman-konteks untuk teks bahasa Indonesia.

Dirancang agar fungsi gramatikal murni (di, ke, dari, yang, ini, itu)
dibuang, tetapi konteks pembuka kalimat dan kata negasi tidak rusak.
"""


from src.utils.config import Config
from src.utils.logger import Logger


class StopwordFilter:
    """
    Menghapus kata fungsi (stopword) dari daftar token dengan proteksi konteks.

    Aturan proteksi:
        1. Token pada posisi lead (awal kalimat) tidak dihapus — bagian ini
           umumnya menetapkan topik/target ujaran.
        2. Kata negasi (tidak, bukan, jangan, tak) tidak pernah dihapus dan
           dijaga dari daftar stopword saat loading.
        3. Rasio penghapusan dibatasi; jika teks terlalu pendek atau
           seluruh isinya stopword, token asli dikembalikan (fallback).

    Attributes:
        stopwords (Set[str]): Kumpulan kata fungsi yang dibuang.
        lead_protect (int): Jumlah token awal yang dipertahankan utuh.
        min_keep_ratio (float): Proporsi minimum token yang wajib tersisa.
    """

    NEGATION_TOKENS: set[str] = {"tidak", "bukan", "jangan", "tak", "anti"}

    def __init__(
        self,
        stopwords: set[str] | None = None,
        lead_protect: int = 3,
        min_keep_ratio: float = 0.4,
        config: Config | None = None,
    ) -> None:
        """
        Inisialisasi filter stopword.

        Args:
            stopwords (Set[str], optional): Kustom set stopword. Jika None,
                dimuat dari Config.STOPWORDS_PATH.
            lead_protect (int): Banyak token awal yang dilindungi.
            min_keep_ratio (float): Rasio minimum token yang harus tersisa;
                di bawah nilai ini, fallback ke token asli.
            config (Config, optional): Instance konfigurasi terpusat.
        """
        self.config = config or Config()
        self.logger = Logger.get_logger("StopwordFilter")
        self.lead_protect = lead_protect
        self.min_keep_ratio = min_keep_ratio
        self.stopwords: set[str] = stopwords if stopwords is not None \
            else self._load_stopwords(self.config.STOPWORDS_PATH)
        # Guard: negation tokens tidak boleh pernah jadi stopword
        self.stopwords -= self.NEGATION_TOKENS
        self.logger.info(f"Stopwords termuat: {len(self.stopwords)} kata "
                         f"(negation guard aktif).")

    @staticmethod
    def _load_stopwords(path: str) -> set[str]:
        """
        Membaca daftar stopword dari file teks (satu kata per baris).

        Args:
            path (str): Lokasi file stopword.

        Returns:
            Set[str]: Kumpulan stopword.
        """
        with open(path, encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}

    def filter_tokens(self, tokens: list[str]) -> list[str]:
        """
        Menghapus stopword dari daftar token dengan proteksi konteks.

        Args:
            tokens (List[str]): Daftar token hasil tokenisasi.

        Returns:
            List[str]: Daftar token tersaring (atau asli bila rasio terlalu
                rendah — fallback pengaman konteks).
        """
        if not tokens:
            return []

        kept: list[str] = []
        for i, tok in enumerate(tokens):
            if i < self.lead_protect:
                # konteks pembuka selalu dipertahankan
                kept.append(tok)
                continue
            if tok.lower() in self.stopwords:
                continue
            kept.append(tok)

        if len(kept) < max(1, int(len(tokens) * self.min_keep_ratio)):
            # terlalu agresif — kembalikan token asli
            return list(tokens)
        return kept

    def filter_text(self, text: str) -> str:
        """
        Filter stopword pada string, mengembalikan string bersih.

        Args:
            text (str): Kalimat utuh.

        Returns:
            str: Kalimat tanpa stopword dengan proteksi konteks.
        """
        return " ".join(self.filter_tokens(text.split()))
