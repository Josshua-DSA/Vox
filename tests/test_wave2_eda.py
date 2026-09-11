"""Tests for subgroup-aware lexical Wave 2 EDA."""

import pandas as pd

from src.eda import TextEDA


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": [
                "kamu hebat sekali",
                "kamu hebat sekali",
                "dasar bodoh kamu",
                "dasar bodoh kamu",
                "hebat bukan toxic",
            ],
            "toxicity": ["[0, 0]", "[0, 1]", "[1, 1]", "[1, 0]", "[0, 0]"],
            "topic": ["A", "A", "B", "B", "A"],
        }
    )


def test_lexical_log_odds_supports_agreement_subset() -> None:
    result = TextEDA().lexical_log_odds(frame(), subset="borderline", min_count=1)

    assert set(result["label"]) == {0, 1}
    assert "log_odds" in result.columns
    assert "document_count" in result.columns


def test_ngram_by_group_keeps_group_identity() -> None:
    result = TextEDA().ngram_by_group(
        frame(), group_column="topic", n=2, min_count=1
    )

    assert set(result["group"]) == {"A", "B"}
    assert "ngram" in result.columns
    assert "toxic_document_rate" in result.columns


def test_kwic_by_group_returns_query_context() -> None:
    result = TextEDA().kwic_by_group(
        frame(), term="hebat", group_column="topic", window=1
    )

    assert set(result["group"]) == {"A"}
    assert result["term"].tolist() == ["hebat", "hebat", "hebat"]
    assert "left_context" in result.columns
    assert "right_context" in result.columns
