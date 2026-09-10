"""Unit test untuk SlangNormalizer (leet, collapse, emoji, slang)."""


class TestSlangNormalizer:
    def test_decode_leet_mixed_digit(self, normalizer):
        result = normalizer.decode_leet("4nj1ng lu")
        assert "anjing" in result

    def test_decode_leet_preserves_legit_numbers(self, normalizer):
        result = normalizer.decode_leet("pilpres 2024 menang")
        assert "2024" in result

    def test_collapse_repeating(self, normalizer):
        result = normalizer.collapse_repeating_chars("begooolll")
        assert result == "begooll"

    def test_collapse_keeps_double_letters(self, normalizer):
        result = normalizer.collapse_repeating_chars("baa sepi")
        assert result == "baa sepi"

    def test_expand_emoji(self, normalizer):
        result = normalizer.expand_emoji("dia😂")
        assert "tertawa" in result

    def test_expand_slang(self, normalizer):
        result = normalizer.expand_slang("gk suka mreka")
        assert "tidak" in result
        assert "mereka" in result

    def test_normalize_full_pipeline(self, normalizer):
        result = normalizer.normalize("4nj1ng emg gk ngerti")
        assert "anjing" in result
        assert "memang" in result
        assert "tidak" in result
