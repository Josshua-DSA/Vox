"""Tests for preprocessing variant signal ablation."""

import pandas as pd

from src.eda import TextEDA


def ablation_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": [
                "anj1ng goblok",
                "anjing goblok",
                "sopan santun",
                "sopan sekali",
            ],
            "toxicity": ["[1, 1]", "[1, 1]", "[0, 0]", "[0, 0]"],
        }
    )


def leet_decode(text: str) -> str:
    return text.replace("1", "i")


def test_signal_ablation_reports_one_row_per_variant() -> None:
    variants = {"raw": lambda text: text, "leet_decode": leet_decode}
    result = TextEDA().variant_signal_ablation(
        ablation_frame(), variants, top_n=2, min_count=1
    )

    assert set(result["variant"]) == {"raw", "leet_decode"}
    for column in (
        "vocabulary_size",
        "raw_vocabulary_overlap",
        "toxic_top_overlap",
        "nontoxic_top_overlap",
    ):
        assert column in result.columns


def test_signal_ablation_identity_variant_preserves_signal() -> None:
    result = TextEDA().variant_signal_ablation(
        ablation_frame(), {"raw": lambda text: text}, top_n=2, min_count=1
    )

    raw = result[result["variant"] == "raw"].iloc[0]
    assert raw["toxic_top_overlap"] == 1.0
    assert raw["raw_vocabulary_overlap"] == 1.0


def test_signal_ablation_collapses_leet_vocabulary() -> None:
    variants = {"raw": lambda text: text, "leet_decode": leet_decode}
    result = TextEDA().variant_signal_ablation(
        ablation_frame(), variants, top_n=2, min_count=1
    )

    raw_vocab = int(result[result["variant"] == "raw"].iloc[0]["vocabulary_size"])
    leet_vocab = int(
        result[result["variant"] == "leet_decode"].iloc[0]["vocabulary_size"]
    )
    assert leet_vocab < raw_vocab
