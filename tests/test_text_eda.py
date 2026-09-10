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


def test_annotation_profile_reports_agreement_and_vote_counts() -> None:
    result = TextEDA().annotation_profile(sample_frame())

    assert result["num_annotators"].tolist() == [2, 2, 2, 2]
    assert result["toxic_votes"].tolist() == [0, 2, 1, 1]
    assert result["agreement_ratio"].tolist() == [1.0, 1.0, 0.5, 0.5]
    assert result["agreement_band"].tolist() == ["unanimous", "unanimous", "borderline", "borderline"]


def test_group_label_rates_supports_topic_conditioning() -> None:
    result = TextEDA().group_label_rates(sample_frame(), group_column="topic")

    umum = result[result["group"] == "Umum"].iloc[0]
    politik = result[result["group"] == "Politik"].iloc[0]
    assert umum["count"] == 3
    assert umum["toxic_rate"] == 2 / 3
    assert politik["toxic_rate"] == 1.0


def test_sublabel_summary_and_cooccurrence_parse_vote_columns() -> None:
    frame = sample_frame()
    frame["insults"] = ["[0, 0]", "[1, 1]", "[1, 0]", "[0, 1]"]
    frame["identity_attack"] = ["[0, 0]", "[0, 0]", "[1, 1]", "[0, 0]"]

    eda = TextEDA()
    summary = eda.sublabel_summary(frame, ["insults", "identity_attack"])
    matrix = eda.sublabel_cooccurrence(frame, ["insults", "identity_attack"])

    assert summary["positive_count"].tolist() == [3, 1]
    assert matrix.loc["insults", "identity_attack"] == 1


def test_duplicate_profile_distinguishes_conflicts() -> None:
    result = TextEDA().duplicate_profile(sample_frame())

    duplicate = result[result["text"] == "Kamu hebat sekali"].iloc[0]
    assert duplicate["duplicate_count"] == 2
    assert bool(duplicate["label_conflict"]) is True


def test_marker_profile_compares_raw_social_text_signals() -> None:
    frame = sample_frame()
    frame.loc[0, "text"] = "HEBAT!!! @user #tag"

    result = TextEDA().marker_profile(frame)

    first = result.iloc[0]
    assert bool(first["has_mention"]) is True
    assert bool(first["has_hashtag"]) is True
    assert bool(first["has_exclamation"]) is True
    assert first["uppercase_ratio"] > 0


def test_variant_comparison_measures_change_without_mutating_raw() -> None:
    frame = sample_frame()
    original = frame.copy(deep=True)

    result = TextEDA().variant_comparison(
        frame,
        variants={"lower": lambda text: text.lower()},
    )

    assert frame.equals(original)
    assert set(result["variant"]) == {"raw", "lower"}
    assert result.loc[result["variant"] == "raw", "document_count"].iloc[0] == 4
    assert "vocabulary_size" in result.columns
    assert "token_retention" in result.columns
