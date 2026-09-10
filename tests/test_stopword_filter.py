"""Unit test untuk StopwordFilter (proteksi konteks lead + negation guard)."""

from src.preprocessing.stopword_filter import StopwordFilter


class TestStopwordFilter:
    def test_removes_function_words_after_lead(self, stopword_filter):
        tokens = ["wajah", "jurnalis", "dibalut", "perban", "saat", "melaporkan"]
        result = stopword_filter.filter_tokens(tokens)
        assert "perban" in result
        assert "melaporkan" in result

    def test_lead_protected(self, stopword_filter):
        tokens = ["di", "ke", "dari", "rumah", "sakit"]
        result = stopword_filter.filter_tokens(tokens)
        assert result[:3] == ["di", "ke", "dari"]

    def test_negation_never_dropped(self, stopword_filter):
        tokens = ["dia", "memang", "tidak", "sukses", "bukan", "gila"]
        result = stopword_filter.filter_tokens(tokens)
        assert "tidak" in result
        assert "bukan" in result

    def test_all_stopword_short_text_fallback(self, stopword_filter):
        strict = StopwordFilter(lead_protect=0)
        tokens = ["dan", "atau", "tapi", "yang"]
        result = strict.filter_tokens(tokens)
        assert len(result) == len(tokens)

    def test_filter_text_returns_string(self, stopword_filter):
        result = stopword_filter.filter_text("rumah sakit itu sangat bagus")
        assert isinstance(result, str)
        assert "rumah" in result
