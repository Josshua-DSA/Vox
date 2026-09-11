"""Tests for punctuation and context marker EDA."""

import pandas as pd

from src.eda import TextEDA


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": ["Kenapa?!", "AMAN!!!", "biasa", "??"],
            "toxicity": ["[1, 1]", "[0, 0]", "[0, 0]", "[1, 0]"],
            "topic": ["A", "A, B", "B", "A"],
        }
    )


def test_marker_detail_preserves_punctuation_counts_and_combinations() -> None:
    result = TextEDA().marker_detail_profile(frame())

    first = result.iloc[0]
    second = result.iloc[1]
    assert first["question_count"] == 1
    assert first["exclamation_count"] == 1
    assert bool(first["has_question_exclamation"]) is True
    assert second["exclamation_run_max"] == 3
    assert result.loc[3, "question_run_max"] == 2


def test_marker_conditioned_rates_support_label_and_agreement() -> None:
    eda = TextEDA()
    result = eda.marker_conditioned_rates(
        frame(), marker="has_question", group_column="label"
    )
    agreement = eda.marker_conditioned_rates(
        frame(), marker="has_question", group_column="agreement_band"
    )

    assert set(result["group"]) == {"0", "1"}
    assert set(agreement["group"]) == {"unanimous", "borderline"}
    assert "marker_rate" in result.columns


def test_marker_conditioned_rates_expands_topic_membership() -> None:
    result = TextEDA().marker_conditioned_rates(
        frame(), marker="has_exclamation", group_column="topic"
    )

    assert set(result["group"]) == {"A", "B"}
    assert result["count"].sum() == 5
    assert result["marker_count"].sum() == 3


def test_marker_detail_does_not_mutate_input() -> None:
    source = frame()
    before = source.copy(deep=True)
    TextEDA().marker_detail_profile(source)
    pd.testing.assert_frame_equal(source, before)



def test_marker_conditioned_rates_rejects_unknown_marker() -> None:
    try:
        TextEDA().marker_conditioned_rates(
            frame(), marker="missing_marker", group_column="label"
        )
    except KeyError as error:
        assert "missing_marker" in str(error)
    else:
        raise AssertionError("unknown marker must raise KeyError")

