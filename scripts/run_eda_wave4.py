"""Run EDA-only leakage-safe split audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.eda import TextEDA
from src.eda.split_audit import audit_split, make_group_split


def run(input_path: Path, output_dir: Path, seed: int = 42) -> None:
    """Create exact-text group split and write audit artifacts."""
    frame = pd.read_csv(input_path)
    eda = TextEDA()
    prepared = eda.prepare_frame(frame)
    prepared["agreement_band"] = eda.annotation_profile(frame)["agreement_band"]
    assigned = make_group_split(prepared, seed=seed)
    assigned.to_csv(output_dir / "wave4_group_split.csv", index=False)

    audit = audit_split(assigned)
    (output_dir / "wave4_split_audit.json").write_text(
        json.dumps(audit, indent=2, default=str) + "\n", encoding="utf-8"
    )

    distribution_rows: list[dict[str, object]] = []
    for split, subset in assigned.groupby("split", sort=True):
        distribution_rows.extend(
            {
                "split": split,
                "metric": metric,
                "value": value,
            }
            for metric, value in {
                "rows": len(subset),
                "label_rate": float(subset["label"].mean()),
                "borderline_rate": float(
                    (subset["agreement_band"] == "borderline").mean()
                ),
                "unanimous_rate": float(
                    (subset["agreement_band"] == "unanimous").mean()
                ),
                "unique_texts": int(subset["text"].nunique()),
            }.items()
        )
    pd.DataFrame(distribution_rows).to_csv(
        output_dir / "wave4_split_distribution.csv", index=False
    )

    topic = (
        assigned.groupby(["split", "topic"], dropna=False)
        .agg(rows=("text", "size"), toxic_rate=("label", "mean"))
        .reset_index()
    )
    topic.to_csv(output_dir / "wave4_topic_distribution.csv", index=False)

    print(f"Wrote {output_dir / 'wave4_group_split.csv'}")
    print(f"Wrote {output_dir / 'wave4_split_audit.json'}")
    print(f"Wrote {output_dir / 'wave4_split_distribution.csv'}")
    print(f"Wrote {output_dir / 'wave4_topic_distribution.csv'}")
    print(json.dumps(audit, indent=2, default=str))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    run(args.input_path, args.output_dir, seed=args.seed)


__all__ = ["run"]
