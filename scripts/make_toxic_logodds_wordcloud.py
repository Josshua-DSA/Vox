"""Create log-odds weighted toxic word clouds from lexical evidence."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


def load_toxic_weights(path: Path, min_count: int) -> Counter[str]:
    """Load document-presence log-odds weights for toxic tokens."""
    frame = pd.read_csv(path)
    toxic = frame[(frame["subset"] == "all") & (frame["label"] == 1)].copy()
    toxic = toxic[toxic["token"].astype(str).str.len() >= 3]
    toxic = toxic[toxic["document_count"] >= min_count]
    toxic = toxic[toxic["log_odds"] > 0]
    weights = Counter(
        {str(token): float(score) for token, score in zip(toxic["token"], toxic["log_odds"])}
    )
    return weights


def apply_display_stopwords(weights: Counter[str], stopword_path: Path) -> Counter[str]:
    """Remove display-only stopwords without touching lexical evidence."""
    words = {
        line.strip().lower()
        for line in stopword_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    return Counter({token: score for token, score in weights.items() if token not in words})


def write_cloud(counts: Counter[str], path: Path, title: str, top_n: int = 120) -> None:
    """Render a log-odds weighted word cloud."""
    selected = Counter(dict(counts.most_common(top_n)))
    cloud = WordCloud(
        width=1800,
        height=1000,
        background_color="white",
        colormap="magma",
        max_words=top_n,
        min_font_size=12,
        collocations=False,
        random_state=42,
    ).generate_from_frequencies(selected)
    figure, axis = plt.subplots(figsize=(18, 10), dpi=150)
    axis.imshow(cloud, interpolation="bilinear")
    axis.axis("off")
    axis.set_title(title, fontsize=22, pad=18)
    figure.tight_layout(pad=1)
    figure.savefig(path, bbox_inches="tight")
    plt.close(figure)


def run(input_path: Path, output_dir: Path, stopword_path: Path) -> None:
    """Generate toxic log-odds clouds with and without display stopwords."""
    weights = load_toxic_weights(input_path, min_count=10)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_path = output_dir / "toxic_wordcloud_logodds_nostop.png"
    write_cloud(weights, raw_path, "Toxic tokens — log-odds weight, no display stopword")

    filtered = apply_display_stopwords(weights, stopword_path)
    filtered_path = output_dir / "toxic_wordcloud_logodds_clean.png"
    write_cloud(filtered, filtered_path, "Toxic tokens — log-odds weight, display stopwords")

    pd.DataFrame(filtered.most_common(), columns=["token", "log_odds"]).to_csv(
        output_dir / "toxic_wordcloud_logodds_weights.csv", index=False
    )
    print(f"tokens={len(weights)}")
    print(f"filtered_tokens={len(filtered)}")
    print(f"wrote={raw_path}")
    print(f"wrote={filtered_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--stopword-path", type=Path, required=True)
    args = parser.parse_args()
    run(args.input_path, args.output_dir, args.stopword_path)


__all__ = ["run", "load_toxic_weights", "apply_display_stopwords"]
