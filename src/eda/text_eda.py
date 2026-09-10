"""Non-destructive, context-oriented EDA for Indonesian toxic-text data."""

from __future__ import annotations

import ast
import re
from collections import Counter
from typing import Any

import pandas as pd


class TextEDA:
    """Compute text and label summaries without mutating the source DataFrame.

    The class treats preprocessing as an analysis variant. Every method starts
    from a copied frame and keeps raw text available for sentence-level review.
    """

    TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)

    def __init__(
        self,
        text_column: str = "text",
        label_column: str = "label",
        votes_column: str = "toxicity",
        threshold: float = 0.5,
    ) -> None:
        """Configure dataset column names and majority-vote threshold."""
        self.text_column = text_column
        self.label_column = label_column
        self.votes_column = votes_column
        self.threshold = threshold

    def prepare_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return an analysis copy with consensus labels and text metrics.

        Existing ``label`` values are retained. If absent, labels are derived
        from multi-annotator votes in ``toxicity`` using majority voting.
        """
        result = frame.copy(deep=True)
        if self.text_column not in result:
            raise KeyError(f"Missing text column: {self.text_column}")
        if self.label_column not in result:
            if self.votes_column not in result:
                raise KeyError(
                    f"Missing label columns: {self.label_column} or "
                    f"{self.votes_column}"
                )
            result[self.label_column] = result[self.votes_column].map(
                self.consensus_label
            )
        result[self.label_column] = pd.to_numeric(
            result[self.label_column], errors="raise"
        ).astype(int)
        text = result[self.text_column].fillna("").astype(str)
        result["word_count"] = text.map(lambda value: len(self.tokens(value)))
        result["char_count"] = text.str.len()
        result["tokens"] = text.map(self.tokens)
        return result

    def consensus_label(self, votes: Any) -> int:
        """Convert annotator votes into a binary majority label."""
        parsed = self._parse_votes(votes)
        if not parsed:
            return 0
        return int(sum(parsed) / len(parsed) >= self.threshold)

    def label_distribution(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return label counts and percentages."""
        prepared = self.prepare_frame(frame)
        counts = prepared[self.label_column].value_counts().sort_index()
        result = counts.rename("count").to_frame()
        result["percentage"] = result["count"] / len(prepared) * 100
        result.index.name = self.label_column
        return result.reset_index()

    def length_summary(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return word and character length statistics grouped by label."""
        prepared = self.prepare_frame(frame)
        return (
            prepared.groupby(self.label_column)[["word_count", "char_count"]]
            .describe()
            .reset_index()
        )

    def token_counts(self, frame: pd.DataFrame, label: int | None = None) -> pd.DataFrame:
        """Return token frequency and document frequency for one/all labels."""
        prepared = self.prepare_frame(frame)
        if label is not None:
            prepared = prepared[prepared[self.label_column] == label]
        frequency: Counter[str] = Counter()
        documents: Counter[str] = Counter()
        for tokens in prepared["tokens"]:
            frequency.update(tokens)
            documents.update(set(tokens))
        result = pd.DataFrame(
            {
                "token": list(frequency),
                "frequency": list(frequency.values()),
                "document_count": [documents[token] for token in frequency],
            }
        )
        return result.sort_values(
            ["frequency", "token"], ascending=[False, True]
        ).reset_index(drop=True)

    def shared_word_comparison(
        self, frame: pd.DataFrame, min_count: int = 2
    ) -> pd.DataFrame:
        """Compare shared token document counts and rates by binary label."""
        prepared = self.prepare_frame(frame)
        rows: list[dict[str, float | int | str]] = []
        class_sizes = prepared[self.label_column].value_counts().to_dict()
        for token in sorted(set(token for values in prepared["tokens"] for token in values)):
            row: dict[str, float | int | str] = {"token": token}
            for label, name in ((0, "nontoxic"), (1, "toxic")):
                subset = prepared[prepared[self.label_column] == label]
                count = int(subset["tokens"].map(lambda values: token in values).sum())
                row[f"{name}_document_count"] = count
                row[f"{name}_document_rate"] = count / class_sizes.get(label, 1)
            if max(row["toxic_document_count"], row["nontoxic_document_count"]) >= min_count:
                rows.append(row)
        return pd.DataFrame(rows).sort_values("token").reset_index(drop=True)

    def ngram_comparison(
        self, frame: pd.DataFrame, n: int = 2, min_count: int = 2
    ) -> pd.DataFrame:
        """Compare n-gram document counts across labels."""
        if n < 1:
            raise ValueError("n must be at least 1")
        prepared = self.prepare_frame(frame)
        rows: list[dict[str, float | int | str]] = []
        class_sizes = prepared[self.label_column].value_counts().to_dict()
        all_ngrams: set[tuple[str, ...]] = set()
        by_row: list[tuple[int, set[tuple[str, ...]]]] = []
        for label, tokens in zip(prepared[self.label_column], prepared["tokens"]):
            values = set(zip(*(tokens[i:] for i in range(n))))
            by_row.append((int(label), values))
            all_ngrams.update(values)
        for value in sorted(all_ngrams):
            row: dict[str, float | int | str] = {"ngram": " ".join(value)}
            for label, name in ((0, "nontoxic"), (1, "toxic")):
                count = sum(label == current and value in values for current, values in by_row)
                row[f"{name}_document_count"] = count
                row[f"{name}_document_rate"] = count / class_sizes.get(label, 1)
            if max(row["toxic_document_count"], row["nontoxic_document_count"]) >= min_count:
                rows.append(row)
        return pd.DataFrame(rows).sort_values("ngram").reset_index(drop=True)

    def kwic(self, frame: pd.DataFrame, term: str, window: int = 3) -> pd.DataFrame:
        """Return keyword-in-context rows for sentence-level label comparison."""
        if window < 0:
            raise ValueError("window must be non-negative")
        prepared = self.prepare_frame(frame)
        target = term.lower()
        rows: list[dict[str, Any]] = []
        for _, row in prepared.iterrows():
            tokens = row["tokens"]
            for position, token in enumerate(tokens):
                if token == target:
                    rows.append(
                        {
                            "text": row[self.text_column],
                            "label": int(row[self.label_column]),
                            "position": position,
                            "left_context": " ".join(tokens[max(0, position - window):position]),
                            "term": token,
                            "right_context": " ".join(tokens[position + 1:position + 1 + window]),
                        }
                    )
        return pd.DataFrame(rows)

    def conflicting_labels(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Find identical text values assigned to multiple consensus labels."""
        prepared = self.prepare_frame(frame)
        grouped = prepared.groupby(self.text_column, dropna=False)[self.label_column].agg(
            lambda values: tuple(sorted(set(int(value) for value in values)))
        )
        conflicts = grouped[grouped.map(len) > 1]
        return conflicts.rename("labels").reset_index()

    @classmethod
    def tokens(cls, text: str) -> list[str]:
        """Tokenize text for descriptive EDA only; raw text remains unchanged."""
        return [token.lower() for token in cls.TOKEN_PATTERN.findall(text)]

    @staticmethod
    def _parse_votes(votes: Any) -> list[int]:
        if votes is None or (isinstance(votes, float) and pd.isna(votes)):
            return []
        if isinstance(votes, str):
            try:
                votes = ast.literal_eval(votes)
            except (ValueError, SyntaxError):
                votes = [votes]
        if not isinstance(votes, (list, tuple, set)):
            votes = [votes]
        return [int(value) for value in votes if int(value) in (0, 1)]
