"""Run EDA-only punctuation, marker, and context audit."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.eda import TextEDA

MARKERS = [
    "has_question",
    "has_exclamation",
    "has_question_exclamation",
    "has_exclamation_question",
    "has_url",
    "has_mention",
    "has_hashtag",
    "has_emoji_or_symbol",
    "has_repeated_character",
]


def markdown_table(frame: pd.DataFrame) -> str:
    """Render a compact markdown table without optional dependencies."""
    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join(["---"] * len(columns)) + "|",
    ]
    for record in frame.to_dict(orient="records"):
        values = []
        for column in frame.columns:
            value = record[column]
            values.append(f"{value:.4f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def run(input_path: Path, output_dir: Path) -> None:
    """Write detailed marker and conditioned-rate artifacts."""
    frame = pd.read_csv(input_path)
    eda = TextEDA()
    output_dir.mkdir(parents=True, exist_ok=True)

    detail = eda.marker_detail_profile(frame)
    detail["agreement_band"] = eda.annotation_profile(frame)["agreement_band"]
    detail.to_csv(output_dir / "wave6_marker_detail.csv", index=False)

    rate_tables: list[pd.DataFrame] = []
    for group_column in ("label", "agreement_band", "topic"):
        for marker in MARKERS:
            rates = eda.marker_conditioned_rates(
                frame, marker=marker, group_column=group_column
            )
            rate_tables.append(rates)
    all_rates = pd.concat(rate_tables, ignore_index=True)
    all_rates.to_csv(output_dir / "wave6_marker_conditioned_rates.csv", index=False)

    punctuation = detail[
        [
            "text",
            "label",
            "agreement_band",
            "topic",
            "question_count",
            "exclamation_count",
            "question_run_max",
            "exclamation_run_max",
            "has_question_exclamation",
            "has_exclamation_question",
            "punctuation_count",
            "punctuation_density",
            "uppercase_ratio",
        ]
    ].copy()
    evidence = punctuation.sort_values(
        ["punctuation_count", "question_run_max", "exclamation_run_max"],
        ascending=False,
    ).head(300)
    evidence.to_csv(output_dir / "wave6_punctuation_evidence.csv", index=False)

    label_rates = all_rates[all_rates["group_column"] == "label"].copy()
    lines = [
        "# IndoToxic EDA Findings — Wave 6",
        "",
        "Status: punctuation, marker, and context audit; no model training",
        "",
        "## Method",
        "",
        "- Raw text remains unchanged.",
        "- Punctuation is counted, not removed.",
        "- Topic values are expanded as membership for topic-conditioned rates.",
        "- Rates are descriptive and do not establish causal effects.",
        "- Extreme punctuation examples are saved for manual KWIC/context review.",
        "",
        "## Label-conditioned marker rates",
        "",
        markdown_table(label_rates),
        "",
        "## Decision",
        "",
        "- Preserve `?`, `!`, mixed `?!`, repeated punctuation, and punctuation density in raw analysis.",
        "- `remove_punctuation` remains an ablation control, not a default decision.",
        "- Interpret marker signals jointly with agreement and topic context.",
        "- Review `wave6_punctuation_evidence.csv` manually before final preprocessing policy.",
    ]
    try:
        report = "\n".join(lines) + "\n"
    except ImportError:
        report = "\n".join(lines[:12] + ["\nArtifacts contain full tables.\n"])
    (output_dir / "wave6_findings.md").write_text(report, encoding="utf-8")

    print(f"Wrote {output_dir / 'wave6_marker_detail.csv'}")
    print(f"Wrote {output_dir / 'wave6_marker_conditioned_rates.csv'}")
    print(f"Wrote {output_dir / 'wave6_punctuation_evidence.csv'}")
    print(f"Wrote {output_dir / 'wave6_findings.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    run(args.input_path, args.output_dir)


__all__ = ["run", "MARKERS"]
