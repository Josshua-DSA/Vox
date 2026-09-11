"""Run reproducible Wave 1 EDA audits without mutating raw data."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from src.eda import TextEDA
from src.preprocessing import TextCleaner


def collapse_repetition(text: str) -> str:
    """Reduce character runs to at most two characters."""
    return re.sub(r"(.)\1{2,}", r"\1\1", text)


def keep_hashtag_content(text: str) -> str:
    """Remove hashtag marker while preserving hashtag content."""
    return re.sub(r"#(\w+)", r"\1", text)


def run(input_path: Path, output_dir: Path) -> None:
    """Run raw marker and preprocessing-variant comparisons."""
    frame = pd.read_csv(input_path)
    eda = TextEDA()

    marker = eda.marker_profile(frame)
    marker_columns = [
        "has_url",
        "has_mention",
        "has_hashtag",
        "has_exclamation",
        "has_question",
        "has_emoji_or_symbol",
        "has_repeated_character",
    ]
    marker_rows: list[dict[str, int | float | str]] = []
    for column in marker_columns:
        for label in (0, 1):
            values = marker.loc[marker["label"] == label, column]
            marker_rows.append(
                {
                    "marker": column,
                    "label": label,
                    "document_count": len(values),
                    "positive_count": int(values.sum()),
                    "positive_rate": float(values.mean()),
                }
            )
    marker_rates = pd.DataFrame(marker_rows)

    variant_functions = {
        "lowercase": str.lower,
        "keep_hashtag_content": keep_hashtag_content,
        "collapse_repetition": collapse_repetition,
        "existing_cleaner": TextCleaner().clean,
    }
    variants = eda.variant_comparison(frame, variants=variant_functions)
    subgroup_variants = eda.variant_comparison_by_group(
        frame,
        group_columns=["label", "agreement_band"],
        variants=variant_functions,
    )
    topic_membership = eda.topic_membership_rates(frame)

    output_dir.mkdir(parents=True, exist_ok=True)
    marker_rates.to_csv(output_dir / "wave1_marker_rates.csv", index=False)
    variants.to_csv(output_dir / "wave1_variant_comparison.csv", index=False)
    subgroup_variants.to_csv(output_dir / "wave1_variant_by_group.csv", index=False)
    topic_membership.to_csv(output_dir / "wave1_topic_membership_rates.csv", index=False)
    for filename in (
        "wave1_marker_rates.csv",
        "wave1_variant_comparison.csv",
        "wave1_variant_by_group.csv",
        "wave1_topic_membership_rates.csv",
    ):
        print(f"Wrote {output_dir / filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    run(args.input_path, args.output_dir)
