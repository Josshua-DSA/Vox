"""Tests for EDA plot generation."""

from pathlib import Path

import matplotlib
import pandas as pd

from src.eda.plots import TextEDAPlotter

matplotlib.use("Agg")


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": [
                "Kamu hebat sekali",
                "Kamu bodoh sekali",
                "Dasar bodoh kamu",
                "Kamu hebat sekali",
            ],
            "toxicity": ["[0, 0]", "[1, 1]", "[1, 0]", "[0, 1]"],
        }
    )


def test_plotter_writes_label_and_length_figures(tmp_path: Path) -> None:
    plotter = TextEDAPlotter(output_dir=tmp_path)

    label_path = plotter.plot_label_distribution(frame())
    length_path = plotter.plot_length_distributions(frame())

    assert label_path.exists()
    assert length_path.exists()
    assert label_path.suffix == ".png"
    assert length_path.suffix == ".png"


def test_plotter_writes_context_comparison_figures(tmp_path: Path) -> None:
    plotter = TextEDAPlotter(output_dir=tmp_path)

    shared_path = plotter.plot_shared_words(frame(), min_count=1, top_n=5)
    ngram_path = plotter.plot_ngrams(frame(), n=2, min_count=1, top_n=5)

    assert shared_path.exists()
    assert ngram_path.exists()


def test_plotter_rejects_invalid_top_n(tmp_path: Path) -> None:
    plotter = TextEDAPlotter(output_dir=tmp_path)

    try:
        plotter.plot_shared_words(frame(), top_n=0)
    except ValueError as error:
        assert "top_n" in str(error)
    else:
        raise AssertionError("Expected ValueError for top_n=0")
