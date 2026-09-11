"""Regression tests for complete Wave 3 re-audit."""

import pandas as pd

from src.eda import TextEDA


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": ["@a halo! https://x.co #tag", "toxic!!!", "sopan"],
            "toxicity": ["[0, 0]", "[1, 1]", "[0, 0]"],
            "topic": ["A", "A", "B"],
        }
    )


def test_variant_comparison_supports_marker_variants() -> None:
    variants = {
        "remove_url": lambda value: " ".join(
            part for part in value.split() if not part.startswith("http")
        ),
        "remove_mention": lambda value: value.replace("@a", ""),
        "remove_punctuation": lambda value: value.replace("!", ""),
        "remove_emoji": lambda value: value.encode("ascii", "ignore").decode(),
    }
    result = TextEDA().variant_comparison(frame(), variants)
    assert set(variants).issubset(set(result["variant"]))


def test_variant_comparison_by_group_supports_joint_subgroups() -> None:
    data = frame()
    data["agreement_band"] = ["unanimous", "unanimous", "unanimous"]
    result = TextEDA().variant_comparison_by_group(
        data,
        group_columns=["label", "agreement_band", "topic"],
        variants={"raw_copy": lambda value: value},
        combine=True,
    )
    assert "label__agreement_band__topic" in set(result["group_column"])
    assert len(result) == 6


def test_variant_marker_profile_compares_raw_and_transformed_text() -> None:
    result = TextEDA().variant_marker_retention(
        frame(), {"remove_punctuation": lambda value: value.replace("!", "")}
    )
    row = result[result["variant"] == "remove_punctuation"].iloc[0]
    assert row["has_exclamation_rate"] < row["raw_has_exclamation_rate"]
    assert "has_exclamation_delta" in result.columns
