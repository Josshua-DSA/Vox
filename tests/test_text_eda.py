"""Tests for non-destructive, context-oriented text EDA."""

import pandas as pd

from src.eda.text_eda import TextEDA


def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": [
                "Kamu hebat sekali",
                "Kamu bodoh sekali",
                "Dasar bodoh kamu",
                "Kamu hebat sekali",
            ],
            "toxicity": ["[0, 0]", "[1, 1]", "[1, 0]", "[0, 1]"],
            "topic": ["Umum", "Umum", "Politik", "Umum"],
        }
    )


def test_prepare_frame_derives_consensus_and_preserves_input() -> None:
    frame = sample_frame()
    original = frame.copy(deep=True)

    prepared = TextEDA().prepare_frame(frame)

    assert frame.equals(original)
    assert prepared["label"].tolist() == [0, 1, 1, 1]
    assert prepared["word_count"].tolist() == [3, 3, 3, 3]
    assert prepared["char_count"].tolist() == [17, 17, 16, 17]


def test_shared_word_comparison_exposes_both_label_contexts() -> None:
    result = TextEDA().shared_word_comparison(sample_frame(), min_count=1)

    bodoh = result[result["token"] == "bodoh"].iloc[0]
    hebat = result[result["token"] == "hebat"].iloc[0]

    assert bodoh["toxic_document_count"] == 2
    assert bodoh["nontoxic_document_count"] == 0
    assert hebat["toxic_document_count"] == 1
    assert hebat["nontoxic_document_count"] == 1


def test_ngrams_and_kwic_keep_sentence_context() -> None:
    eda = TextEDA()
    ngrams = eda.ngram_comparison(sample_frame(), n=2, min_count=1)
    kwic = eda.kwic(sample_frame(), term="bodoh", window=1)

    assert "dasar bodoh" in ngrams["ngram"].tolist()
    assert kwic["label"].tolist() == [1, 1]
    assert kwic["left_context"].tolist() == ["kamu", "dasar"]
    assert kwic["right_context"].tolist() == ["sekali", "kamu"]


def test_conflicting_labels_identifies_same_text_with_different_labels() -> None:
    result = TextEDA().conflicting_labels(sample_frame())

    assert len(result) == 1
    assert result.iloc[0]["text"] == "Kamu hebat sekali"
    assert result.iloc[0]["labels"] == (0, 1)


def test_label_distribution_reports_counts_and_percentages() -> None:
    result = TextEDA().label_distribution(sample_frame())

    assert result["count"].tolist() == [1, 3]
    assert result["percentage"].round(2).tolist() == [25.0, 75.0]
