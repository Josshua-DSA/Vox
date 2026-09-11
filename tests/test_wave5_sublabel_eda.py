"""Tests for sub-label taxonomy EDA."""

import pandas as pd

from src.eda import TextEDA


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": ["a", "b", "c", "d"],
            "toxicity": ["[1, 1]", "[0, 0]", "[1, 0]", "[0, 0]"],
            "topic": ["A, B", "A", "B", "C"],
            "insults": ["[1, 1]", "[0, 0]", "[1, 1]", "[0, 0]"],
            "identity_attack": ["[0, 0]", "[1, 1]", "[0, 0]", "[0, 0]"],
        }
    )


def test_sublabel_profile_conditions_on_consensus_label() -> None:
    result = TextEDA().sublabel_profile(frame(), ["insults", "identity_attack"])

    insults = result[result["sublabel"] == "insults"].iloc[0]
    assert insults["positive_count"] == 2
    assert insults["toxic_positive_count"] == 2
    assert insults["nontoxic_positive_count"] == 0
    assert "toxic_positive_rate" in result.columns


def test_sublabel_conditioned_rates_support_agreement_and_topic() -> None:
    eda = TextEDA()
    agreement = eda.sublabel_conditioned_rates(
        frame(), ["insults"], group_column="agreement_band"
    )
    topic = eda.sublabel_conditioned_rates(
        frame(), ["insults"], group_column="topic"
    )

    assert set(agreement["group"]) == {"unanimous", "borderline"}
    assert set(topic["group"]) == {"A", "B", "C"}
    assert topic["positive_count"].sum() == 3


def test_sublabel_label_mismatch_reports_non_toxic_positive_rows() -> None:
    result = TextEDA().sublabel_label_mismatch(frame(), ["insults", "identity_attack"])

    insults = result[result["sublabel"] == "insults"].iloc[0]
    identity = result[result["sublabel"] == "identity_attack"].iloc[0]
    assert insults["positive_sublabel_non_toxic"] == 0
    assert identity["positive_sublabel_non_toxic"] == 1
    assert identity["toxic_without_sublabel"] == 2
