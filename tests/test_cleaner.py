"""Unit test untuk sanitasi string pada class TextCleaner."""


class TestTextCleaner:
    def test_clean_urls(self, cleaner):
        text = "Lihat berita di https://t.co/xyz dan http://example.com"
        result = cleaner.clean(text)
        assert "http" not in result
        assert "https" not in result

    def test_clean_mentions(self, cleaner):
        text = "Halo @jokowi dan @prabowo apa kabar?"
        result = cleaner.clean(text)
        assert "@jokowi" not in result
        assert "@prabowo" not in result

    def test_lowercase(self, cleaner):
        text = "TEKS INI HARUS MENJADI LOWERCASE!"
        result = cleaner.clean(text)
        assert result == "teks ini harus menjadi lowercase"

    def test_hashtag_removed_entirely(self, cleaner):
        text = "pakai #IdiotSekali dan #tolol tagar"
        result = cleaner.clean(text)
        assert "idiotsekali" not in result
        assert "tolol" not in result
        assert "tagar" in result

    def test_non_string_returns_empty(self, cleaner):
        assert cleaner.clean(None) == ""
        assert cleaner.clean(123) == ""
