"""Create toxic-only cleaned word clouds without mutating raw data."""

from __future__ import annotations

import argparse
import ast
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MENTION_RE = re.compile(r"@[\w_]+")
TOKEN_RE = re.compile(r"[a-zA-ZÀ-ÿ]+(?:'[a-zA-ZÀ-ÿ]+)?")
NEGATIONS = {"tidak", "bukan", "jangan", "tak", "anti"}


def consensus_label(value: str) -> int:
    """Return majority-vote toxicity label from serialized votes."""
    votes = [int(item) for item in ast.literal_eval(str(value))]
    return int(sum(votes) / len(votes) >= 0.5)


def load_stopwords(path: Path) -> set[str]:
    """Load Indonesian stopwords while protecting negation terms."""
    words = {
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    return words


MIN_TOKEN_LENGTH = 3
MIN_DOCUMENT_COUNT = 5


def clean_tokens(text: str, stopwords: set[str]) -> list[str]:
    """Create display tokens; preserve hashtag content, remove visual noise."""
    text = URL_RE.sub(" ", str(text).lower())
    text = MENTION_RE.sub(" ", text)
    text = text.replace("#", " ")
    tokens = TOKEN_RE.findall(text)
    cleaned = []
    for token in tokens:
        if len(token) < MIN_TOKEN_LENGTH:
            continue
        if token in stopwords:
            continue
        cleaned.append(token)
    return cleaned


def frequencies(frame: pd.DataFrame, stopwords: set[str], unique_text: bool) -> Counter[str]:
    """Count cleaned tokens from toxic rows, optionally one count per text."""
    texts = frame["text"].fillna("").astype(str)
    if unique_text:
        texts = texts.drop_duplicates()
    counts: Counter[str] = Counter()
    for text in texts:
        counts.update(set(clean_tokens(text, stopwords)))
    return counts


def write_cloud(counts: Counter[str], path: Path, title: str, cmap: str) -> None:
    """Render one word cloud from document-presence frequencies."""
    cloud = WordCloud(
        width=1800,
        height=1000,
        background_color="white",
        colormap=cmap,
        max_words=120,
        min_font_size=12,
        collocations=False,
        random_state=42,
    ).generate_from_frequencies(counts)
    figure, axis = plt.subplots(figsize=(18, 10), dpi=150)
    axis.imshow(cloud, interpolation="bilinear")
    axis.axis("off")
    axis.set_title(title, fontsize=22, pad=18)
    figure.tight_layout(pad=1)
    figure.savefig(path, bbox_inches="tight")
    plt.close(figure)


def run(input_path: Path, output_dir: Path, stopword_path: Path) -> None:
    """Generate row-weighted and unique-text toxic word clouds."""
    frame = pd.read_csv(input_path)
    frame["_label"] = frame["toxicity"].map(consensus_label)
    toxic = frame[frame["_label"] == 1].copy()
    stopwords = load_stopwords(stopword_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = []
    for unique_text, suffix, title in (
        (False, "rows", "Toxic class — cleaned tokens, all rows"),
        (True, "unique", "Toxic class — cleaned tokens, unique texts"),
    ):
        counts = frequencies(toxic, stopwords, unique_text=unique_text)
        counts = Counter(
            {token: count for token, count in counts.items() if count >= MIN_DOCUMENT_COUNT}
        )
        path = output_dir / f"toxic_wordcloud_clean_{suffix}.png"
        write_cloud(counts, path, title, "magma")
        rows = pd.DataFrame(counts.most_common(), columns=["token", "document_count"])
        rows.insert(0, "weighting", suffix)
        outputs.append(rows)

    pd.concat(outputs, ignore_index=True).to_csv(
        output_dir / "toxic_wordcloud_clean_frequencies.csv", index=False
    )
    (output_dir / "toxic_wordcloud_readme.md").write_text(
        "# Toxic-only WordCloud\n\n"
        "Cleaning is display-only: lowercase, URL/mention removal, hashtag-content preservation, "
        "punctuation/symbol removal, and Indonesian stopword removal. Raw data is unchanged.\n\n"
        "`rows` keeps duplicate-row weighting. `unique` counts each exact text once as a sensitivity view.\n",
        encoding="utf-8",
    )
    print(f"toxic_rows={len(toxic)}")
    print(f"unique_toxic_texts={toxic['text'].nunique()}")
    for name in ("toxic_wordcloud_clean_rows.png", "toxic_wordcloud_clean_unique.png"):
        print(f"wrote={output_dir / name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--stopword-path", type=Path, required=True)
    args = parser.parse_args()
    run(args.input_path, args.output_dir, args.stopword_path)


__all__ = ["run", "clean_tokens", "consensus_label"]
