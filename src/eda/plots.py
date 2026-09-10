"""Focused plots for iterative, context-oriented text EDA."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.eda.text_eda import TextEDA


class TextEDAPlotter:
    """Generate saved EDA plots while delegating calculations to ``TextEDA``."""

    LABEL_NAMES = {0: "Non-toxic", 1: "Toxic"}

    def __init__(self, output_dir: str | Path = "outputs/eda") -> None:
        """Create a plotter and ensure its output directory exists."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.eda = TextEDA()
        sns.set_theme(style="whitegrid")

    def plot_label_distribution(self, frame: pd.DataFrame) -> Path:
        """Save absolute label counts with readable class names."""
        data = self.eda.label_distribution(frame)
        data["class"] = data["label"].map(self.LABEL_NAMES).fillna(data["label"].astype(str))
        figure, axis = plt.subplots(figsize=(7, 5))
        sns.barplot(data=data, x="class", y="count", ax=axis, color="#4472C4")
        axis.set(title="Label distribution", xlabel="Label", ylabel="Documents")
        self._annotate_bars(axis)
        return self._save(figure, "label_distribution.png")

    def plot_length_distributions(self, frame: pd.DataFrame) -> Path:
        """Save word-count and character-count distributions by label."""
        data = self.eda.prepare_frame(frame)
        long = data[["label", "word_count", "char_count"]].melt(
            id_vars="label", var_name="measure", value_name="value"
        )
        long["class"] = long["label"].map(self.LABEL_NAMES).fillna(long["label"].astype(str))
        figure, axes = plt.subplots(1, 2, figsize=(12, 5))
        for axis, measure in zip(axes, ("word_count", "char_count")):
            subset = long[long["measure"] == measure]
            sns.boxplot(data=subset, x="class", y="value", ax=axis)
            axis.set(title=f"{measure.replace('_', ' ').title()} by label", xlabel="Label", ylabel=measure)
        figure.tight_layout()
        return self._save(figure, "length_distributions.png")

    def plot_shared_words(
        self, frame: pd.DataFrame, min_count: int = 2, top_n: int = 20
    ) -> Path:
        """Save normalized document-rate comparison for shared words."""
        if top_n < 1:
            raise ValueError("top_n must be at least 1")
        data = self.eda.shared_word_comparison(frame, min_count=min_count).copy()
        if data.empty:
            return self._empty_plot("No words meet min_count", "shared_words.png")
        data["contrast"] = (
            data["toxic_document_rate"] - data["nontoxic_document_rate"]
        ).abs()
        data = data.nlargest(top_n, "contrast").sort_values("contrast")
        plot_data = data.melt(
            id_vars="token",
            value_vars=["nontoxic_document_rate", "toxic_document_rate"],
            var_name="class",
            value_name="document_rate",
        )
        plot_data["class"] = plot_data["class"].str.replace(
            "_document_rate", "", regex=False
        ).map({"nontoxic": "Non-toxic", "toxic": "Toxic"})
        figure, axis = plt.subplots(figsize=(10, 7))
        sns.barplot(data=plot_data, x="document_rate", y="token", hue="class", ax=axis)
        axis.set(title="Shared words: document-rate comparison", xlabel="Document rate", ylabel="Token")
        figure.tight_layout()
        return self._save(figure, "shared_words.png")

    def plot_ngrams(
        self, frame: pd.DataFrame, n: int = 2, min_count: int = 2, top_n: int = 20
    ) -> Path:
        """Save n-gram document-rate comparison by label."""
        if top_n < 1:
            raise ValueError("top_n must be at least 1")
        data = self.eda.ngram_comparison(frame, n=n, min_count=min_count).copy()
        if data.empty:
            return self._empty_plot("No n-grams meet min_count", f"{n}grams.png")
        data["contrast"] = (
            data["toxic_document_rate"] - data["nontoxic_document_rate"]
        ).abs()
        data = data.nlargest(top_n, "contrast").sort_values("contrast")
        plot_data = data.melt(
            id_vars="ngram",
            value_vars=["nontoxic_document_rate", "toxic_document_rate"],
            var_name="class",
            value_name="document_rate",
        )
        plot_data["class"] = plot_data["class"].str.replace(
            "_document_rate", "", regex=False
        ).map({"nontoxic": "Non-toxic", "toxic": "Toxic"})
        figure, axis = plt.subplots(figsize=(10, 7))
        sns.barplot(data=plot_data, x="document_rate", y="ngram", hue="class", ax=axis)
        axis.set(title=f"Top {n}-grams: document-rate comparison", xlabel="Document rate", ylabel=f"{n}-gram")
        figure.tight_layout()
        return self._save(figure, f"{n}grams.png")

    @staticmethod
    def _annotate_bars(axis: plt.Axes) -> None:
        for container in axis.containers:
            axis.bar_label(container, fmt="%.0f", padding=3)

    def _empty_plot(self, message: str, filename: str) -> Path:
        figure, axis = plt.subplots(figsize=(8, 4))
        axis.text(0.5, 0.5, message, ha="center", va="center")
        axis.set_axis_off()
        return self._save(figure, filename)

    def _save(self, figure: plt.Figure, filename: str) -> Path:
        path = self.output_dir / filename
        figure.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(figure)
        return path
