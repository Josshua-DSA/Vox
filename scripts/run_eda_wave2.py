"""Run reproducible Wave 2 lexical and context EDA audits."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.eda import TextEDA

LEXICAL_SUBSETS = ("all", "unanimous", "borderline")


def expand_topic_membership(frame: pd.DataFrame) -> pd.DataFrame:
    """Expand comma-separated topics for analysis without mutating input."""
    records: list[dict[str, object]] = []
    for record in frame.to_dict(orient="records"):
        value = record.get("topic")
        topics = [
            part.strip()
            for part in str(value if pd.notna(value) else "UNKNOWN").split(",")
            if part.strip()
        ] or ["UNKNOWN"]
        records.extend({**record, "topic_membership": topic} for topic in topics)
    return pd.DataFrame(records)


def top_toxic_terms(lexical: pd.DataFrame, limit: int = 12) -> list[str]:
    """Select frequent positive-label terms for KWIC evidence."""
    selected = lexical.loc[
        (lexical["label"] == 1) & (lexical["log_odds"] > 0)
    ].sort_values(["document_count", "log_odds"], ascending=False)
    return selected["token"].drop_duplicates().head(limit).tolist()


def write_findings(
    output_dir: Path,
    lexical: dict[str, pd.DataFrame],
    agreement_ngrams: pd.DataFrame,
    topic_ngrams: pd.DataFrame,
    kwic: pd.DataFrame,
) -> None:
    """Write Wave 2 interpretation checkpoint."""
    lines = [
        "# IndoToxic EDA Findings — Wave 2",
        "",
        "Status: exploratory lexical/context checkpoint",
        "",
        "## Method",
        "",
        "- Lexical contrast uses document-presence log-odds with additive smoothing 0.5.",
        "- Results are separated into `all`, `unanimous`, and `borderline` subsets.",
        "- N-grams use document rates, not raw token totals.",
        "- Comma-separated topics are expanded as membership for analysis only.",
        "- KWIC preserves raw sentence evidence for manual review.",
        "",
        "## Evidence summary",
        "",
    ]
    for subset, table in lexical.items():
        toxic = table.loc[table["label"] == 1].nlargest(10, "log_odds")
        non_toxic = table.loc[table["label"] == 0].nlargest(10, "log_odds")
        lines.extend(
            [
                f"### {subset.title()} lexical contrast",
                "",
                f"- Rows: {len(table):,}",
                "- Toxic-associated: "
                + (", ".join(f"`{v}`" for v in toxic["token"]) or "none"),
                "- Non-toxic-associated: "
                + (", ".join(f"`{v}`" for v in non_toxic["token"]) or "none"),
                "",
            ]
        )
    lines.extend(
        [
            "### N-gram context",
            "",
            f"- Agreement-band rows: {len(agreement_ngrams):,}",
            f"- Topic-membership rows: {len(topic_ngrams):,}",
            "- Inspect support counts and KWIC before treating n-grams as toxic cues.",
            "",
            "### KWIC",
            "",
            f"- Evidence rows: {len(kwic):,}",
            "- Check insult, quotation, negation, and topic-dependent usage manually.",
            "",
            "## Next experiment",
            "",
            "- Keep punctuation, hashtag content, emoji, and repetition as parallel variants.",
            "- Compare variants within unanimous and borderline subsets.",
            "- Do not turn lexical log-odds into an automatic removal list.",
        ]
    )
    (output_dir / "wave2_findings.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def run(input_path: Path, output_dir: Path, min_count: int = 20) -> None:
    """Run Wave 2 lexical, n-gram, and KWIC analyses."""
    frame = pd.read_csv(input_path)
    eda = TextEDA()
    output_dir.mkdir(parents=True, exist_ok=True)

    lexical = {
        subset: eda.lexical_log_odds(frame, subset=subset, min_count=min_count)
        for subset in LEXICAL_SUBSETS
    }
    for subset, table in lexical.items():
        table.to_csv(output_dir / f"wave2_lexical_log_odds_{subset}.csv", index=False)

    agreement_frame = frame.copy(deep=True)
    agreement_frame["agreement_band"] = eda.annotation_profile(frame)["agreement_band"]
    agreement_ngrams = eda.ngram_by_group(
        agreement_frame, "agreement_band", n=2, min_count=min_count
    )
    agreement_ngrams.to_csv(
        output_dir / "wave2_bigrams_by_agreement.csv", index=False
    )

    topic_frame = expand_topic_membership(frame)
    topic_ngrams = eda.ngram_by_group(
        topic_frame, "topic_membership", n=2, min_count=min_count
    )
    topic_ngrams.to_csv(output_dir / "wave2_bigrams_by_topic.csv", index=False)

    kwic_parts: list[pd.DataFrame] = []
    for term in top_toxic_terms(lexical["all"]):
        evidence = eda.kwic_by_group(frame, term, "topic", window=4)
        if not evidence.empty:
            evidence = evidence.assign(query_term=term)
            kwic_parts.append(evidence.groupby("query_term", sort=False).head(25))
    kwic = pd.concat(kwic_parts, ignore_index=True) if kwic_parts else pd.DataFrame()
    kwic.to_csv(output_dir / "wave2_kwic_evidence.csv", index=False)

    write_findings(output_dir, lexical, agreement_ngrams, topic_ngrams, kwic)
    print(f"Wrote {len(lexical)} lexical tables")
    print(f"Wrote {len(agreement_ngrams):,} agreement n-grams")
    print(f"Wrote {len(topic_ngrams):,} topic n-grams")
    print(f"Wrote {len(kwic):,} KWIC rows")
    print(f"Wrote {output_dir / 'wave2_findings.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--min-count", type=int, default=20)
    args = parser.parse_args()
    run(args.input_path, args.output_dir, min_count=args.min_count)


__all__ = ["expand_topic_membership", "run", "top_toxic_terms", "write_findings"]
