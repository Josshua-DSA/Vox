import unittest
from src.preprocessing.cleaner import TextCleaner


class TestTextCleaner(unittest.TestCase):
    """Unit test untuk sanitasi string pada class TextCleaner."""

    def setUp(self) -> None:
        self.cleaner = TextCleaner()

    def test_clean_urls(self) -> None:
        text = "Lihat berita di https://t.co/xyz dan http://example.com"
        result = self.cleaner.clean(text)
        self.assertNotIn("http", result)
        self.assertNotIn("https", result)

    def test_clean_mentions(self) -> None:
        text = "Halo @jokowi dan @prabowo apa kabar?"
        result = self.cleaner.clean(text)
        self.assertNotIn("@jokowi", result)
        self.assertNotIn("@prabowo", result)

    def test_lowercase(self) -> None:
        text = "TEKS INI HARUS MENJADI LOWERCASE!"
        result = self.cleaner.clean(text)
        self.assertEqual(result, "teks ini harus menjadi lowercase")


if __name__ == "__main__":
    unittest.main()
