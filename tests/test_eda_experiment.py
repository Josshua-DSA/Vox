"""Tests for subgroup-aware EDA experiments."""

import pandas as pd

from src.eda import TextEDA


def experiment_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": [
                "BAGUS!!!",
                "bagus",
                "jelek???",
                "jelek",
            ],
            "toxicity": ["[0, 0]", "[0, 1]", "[1, 0]", "[1, 1]"],
            "topic": ["A", "A", "B", "B"],
        }
    )


def test_variant_comparison_by_group_preserves_raw_and_reports_rates() -> None:
    frame = experiment_frame()
    original = frame.copy(deep=True)

    result = TextEDA().variant_comparison_by_group(
        frame,
        group_columns=["label", "agreement_band"],
        variants={"lowercase": str.lower},
    )

    assert frame.equals(original)
    assert set(result["variant"]) == {"raw", "lowercase"}
    assert set(result["group_column"]) == {"label", "agreement_band"}
    assert "token_retention" in result.columns
    assert "vocabulary_size" in result.columns


def test_topic_membership_rates_split_multi_topic_values() -> None:
    frame = experiment_frame()
    frame.loc[0, "topic"] = "A, B"

    result = TextEDA().topic_membership_rates(frame, "topic")

    both = result[result["topic"] == "B"].iloc[0]
    assert both["count"] == 3
    assert both["toxic_count"] == 2
