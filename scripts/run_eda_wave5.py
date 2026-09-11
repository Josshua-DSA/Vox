"""Run EDA-only sub-label taxonomy audit."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.eda import TextEDA

SUBLABELS = [
    "profanity_obscenity",
    "threat_incitement_to_violence",
    "insults",
    "identity_attack",
    "sexually_explicit",
]


def markdown_table(frame: pd.DataFrame) -> str:
    """Render compact DataFrame markdown without optional dependencies."""
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
    """Run sub-label profiles, conditioned rates, and mismatch audit."""
    frame = pd.read_csv(input_path)
    eda = TextEDA()
    output_dir.mkdir(parents=True, exist_ok=True)

    profile = eda.sublabel_profile(frame, SUBLABELS)
    profile.to_csv(output_dir / "wave5_sublabel_profile.csv", index=False)

    cooccurrence = eda.sublabel_cooccurrence(frame, SUBLABELS)
    cooccurrence.to_csv(output_dir / "wave5_sublabel_cooccurrence.csv")

    prepared = frame.copy(deep=True)
    prepared["agreement_band"] = eda.annotation_profile(frame)["agreement_band"]
    agreement = eda.sublabel_conditioned_rates(
        prepared, SUBLABELS, group_column="agreement_band"
    )
    agreement.to_csv(output_dir / "wave5_sublabel_by_agreement.csv", index=False)

    topic = eda.sublabel_conditioned_rates(frame, SUBLABELS, group_column="topic")
    topic.to_csv(output_dir / "wave5_sublabel_by_topic.csv", index=False)

    mismatch = eda.sublabel_label_mismatch(frame, SUBLABELS)
    mismatch.to_csv(output_dir / "wave5_sublabel_label_mismatch.csv", index=False)

    lines = [
        "# IndoToxic EDA Findings — Wave 5",
        "",
        "Status: sub-label taxonomy audit; no model training",
        "",
        "## Method",
        "",
        "- Sub-label votes use same majority threshold as primary toxicity label.",
        "- Topic values are expanded as membership for conditioned descriptive rates.",
        "- Non-toxic sub-label positives are retained as annotation evidence, not removed.",
        "- Co-occurrence counts are row-level joint-positive counts.",
        "",
        "## Sub-label profile",
        "",
        markdown_table(profile),
        "",
        "## Label mismatch",
        "",
        markdown_table(mismatch),
        "",
        "## Agreement-conditioned rates",
        "",
        markdown_table(agreement),
        "",
        "## Decision",
        "",
        "- Treat sub-labels as descriptive taxonomy, not automatically equivalent to primary toxicity.",
        "- Audit non-toxic sub-label positives before using them as auxiliary targets.",
        "- Preserve co-occurrence structure; one text may express multiple categories.",
        "- Use topic-conditioned tables to separate category prevalence from topic composition.",
    ]
    (output_dir / "wave5_findings.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    print(f"Wrote {output_dir / 'wave5_sublabel_profile.csv'}")
    print(f"Wrote {output_dir / 'wave5_sublabel_cooccurrence.csv'}")
    print(f"Wrote {output_dir / 'wave5_sublabel_by_agreement.csv'}")
    print(f"Wrote {output_dir / 'wave5_sublabel_by_topic.csv'}")
    print(f"Wrote {output_dir / 'wave5_sublabel_label_mismatch.csv'}")
    print(f"Wrote {output_dir / 'wave5_findings.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    run(args.input_path, args.output_dir)


__all__ = ["run", "SUBLABELS"]
