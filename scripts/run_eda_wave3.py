"""Run reproducible Wave 3 preprocessing variant signal ablation."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from src.eda import TextEDA
from src.preprocessing import SlangNormalizer, TextCleaner


def keep_hashtag_content(text: str) -> str:
    """Strip the '#' marker but keep the hashtag word."""
    return re.sub(r"#(\w+)", r"\1", text)


def remove_hashtag(text: str) -> str:
    """Remove the hashtag marker and its content entirely."""
    return re.sub(r"#\w+", " ", text)


def remove_url(text: str) -> str:
    """Remove URL while preserving surrounding text."""
    return re.sub(r"https?://\S+|www\.\S+", " ", text)


def remove_mention(text: str) -> str:
    """Remove @mention token."""
    return re.sub(r"@\w+", " ", text)


def remove_punctuation(text: str) -> str:
    """Remove non-word punctuation and symbols."""
    return re.sub(r"[^\w\s]", " ", text)


def remove_emoji(text: str) -> str:
    """Remove non-ASCII symbols as conservative emoji proxy."""
    return text.encode("ascii", "ignore").decode()


def build_variants() -> dict[str, Callable[[str], str]]:
    """Return single-purpose variants built from the production preprocessors.

    Lexicon paths resolve from this file's repository root so the function
    works from any working directory (runner CLI and notebook alike).
    """
    resources = Path(__file__).resolve().parent.parent / "data" / "resources"
    normalizer = SlangNormalizer(
        slang_dict=json.loads(
            (resources / "slang_dict.json").read_text(encoding="utf-8")
        ),
        emoji_map=json.loads(
            (resources / "emoji_map.json").read_text(encoding="utf-8")
        ),
    )
    cleaner = TextCleaner()
    return {
        "lowercase": str.lower,
        "leet_decode": normalizer.decode_leet,
        "collapse_repetition": normalizer.collapse_repeating_chars,
        "expand_emoji": normalizer.expand_emoji,
        "expand_slang": normalizer.expand_slang,
        "keep_hashtag_content": keep_hashtag_content,
        "remove_hashtag": remove_hashtag,
        "remove_url": remove_url,
        "remove_mention": remove_mention,
        "remove_punctuation": remove_punctuation,
        "remove_emoji": remove_emoji,
        "full_normalize": normalizer.normalize,
        "existing_cleaner": cleaner.clean,
    }


def markdown_table(frame: pd.DataFrame) -> str:
    """Render a DataFrame as a GitHub markdown table without tabulate."""
    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join(["---"] * len(columns)) + "|",
    ]
    for record in frame.to_dict(orient="records"):
        cells = []
        for column in frame.columns:
            value = record[column]
            if isinstance(value, float):
                text = f"{value:.4f}"
            else:
                text = str(value)
            cells.append(text.replace("|", "\\|"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_findings(
    output_dir: Path,
    ablation: pd.DataFrame,
    by_group: pd.DataFrame,
    marker_retention: pd.DataFrame,
) -> None:
    """Write Wave 3 interpretation checkpoint."""
    lines = [
        "# IndoToxic EDA Findings — Wave 3",
        "",
        "Status: preprocessing variant signal ablation",
        "",
        "## Method",
        "",
        "- Each variant is a single-purpose transform applied to raw text.",
        "- Signal preservation compares top-N discriminating tokens (document-presence",
        "  log-odds) against the raw baseline via Jaccard overlap.",
        "- `raw_vocabulary_overlap` = variant vocab retained from raw vocab.",
        "- Vocabulary collapse is expected for leet/slang normalization (merges",
        "  obfuscated forms); a drop in overlap without collapse signals signal loss.",
        "",
        "## Signal ablation",
        "",
        markdown_table(ablation),
        "",
        "## Agreement-stratified vocabulary retention",
        "",
        markdown_table(by_group),
        "",
        "## Marker retention",
        "",
        markdown_table(marker_retention),
        "",
        "## Reading",
        "",
        "- High `toxic_top_overlap` + vocabulary collapse = safe normalization.",
        "- Low `toxic_top_overlap` = the variant removes or rewrites toxic cues.",
        "- Removing hashtags or punctuation must be checked against KWIC before adoption.",
    ]
    (output_dir / "wave3_findings.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def run(
    input_path: Path, output_dir: Path, top_n: int = 20, min_count: int = 20
) -> None:
    """Run Wave 3 signal ablation and stratified vocabulary retention."""
    frame = pd.read_csv(input_path)
    eda = TextEDA()
    output_dir.mkdir(parents=True, exist_ok=True)

    variants = build_variants()
    ablation = eda.variant_signal_ablation(
        frame, variants=variants, top_n=top_n, min_count=min_count
    )
    ablation.to_csv(output_dir / "wave3_signal_ablation.csv", index=False)

    group_frame = frame.copy(deep=True)
    group_frame["agreement_band"] = eda.annotation_profile(frame)["agreement_band"]
    by_group = eda.variant_comparison_by_group(
        group_frame,
        group_columns=["label", "agreement_band", "topic"],
        variants=variants,
        combine=True,
    )
    by_group.to_csv(output_dir / "wave3_vocab_retention_joint_groups.csv", index=False)

    marker_retention = eda.variant_marker_retention(frame, variants)
    marker_retention.to_csv(output_dir / "wave3_marker_retention.csv", index=False)

    write_findings(output_dir, ablation, by_group, marker_retention)
    print(ablation.to_string(index=False))
    print(f"Wrote {output_dir / 'wave3_signal_ablation.csv'}")
    print(f"Wrote {output_dir / 'wave3_vocab_retention_joint_groups.csv'}")
    print(f"Wrote {output_dir / 'wave3_marker_retention.csv'}")
    print(f"Wrote {output_dir / 'wave3_findings.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--min-count", type=int, default=20)
    args = parser.parse_args()
    run(args.input_path, args.output_dir, top_n=args.top_n, min_count=args.min_count)


__all__ = ["build_variants", "keep_hashtag_content", "remove_hashtag", "run"]
