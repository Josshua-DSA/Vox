"""Non-destructive, context-oriented EDA for Indonesian toxic-text data."""

from __future__ import annotations

import ast
import math
import re
from collections import Counter
from collections.abc import Callable
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

    def annotation_profile(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Summarize vote count and agreement for each text row."""
        if self.votes_column not in frame:
            raise KeyError(f"Missing votes column: {self.votes_column}")
        result = frame.copy(deep=True)
        parsed = result[self.votes_column].map(self._parse_votes)
        result["num_annotators"] = parsed.map(len)
        result["toxic_votes"] = parsed.map(sum)
        result["nontoxic_votes"] = result["num_annotators"] - result["toxic_votes"]
        result["agreement_ratio"] = parsed.map(self._agreement_ratio)
        result["agreement_band"] = result["agreement_ratio"].map(
            lambda value: "unrated" if pd.isna(value) else (
                "unanimous" if value == 1.0 else "borderline"
            )
        )
        return result

    def group_label_rates(
        self, frame: pd.DataFrame, group_column: str, min_count: int = 1
    ) -> pd.DataFrame:
        """Calculate sample count and toxic rate conditioned on a column."""
        if min_count < 1:
            raise ValueError("min_count must be at least 1")
        prepared = self.prepare_frame(frame)
        if group_column not in prepared:
            raise KeyError(f"Missing group column: {group_column}")
        groups = prepared[group_column].fillna("UNKNOWN").astype(str)
        grouped = prepared.assign(_group=groups).groupby("_group")[self.label_column]
        result = grouped.agg(count="size", toxic_count="sum").reset_index()
        result = result.rename(columns={"_group": "group"})
        result["toxic_rate"] = result["toxic_count"] / result["count"]
        return result[result["count"] >= min_count].reset_index(drop=True)

    def sublabel_summary(
        self, frame: pd.DataFrame, columns: list[str]
    ) -> pd.DataFrame:
        """Summarize consensus-positive counts for sub-label vote columns."""
        rows: list[dict[str, int | float | str]] = []
        for column in columns:
            if column not in frame:
                raise KeyError(f"Missing sub-label column: {column}")
            labels = frame[column].map(self.consensus_label)
            positive_count = int(labels.sum())
            rows.append(
                {
                    "sublabel": column,
                    "positive_count": positive_count,
                    "positive_rate": positive_count / len(frame) if len(frame) else 0.0,
                }
            )
        return pd.DataFrame(rows)

    def sublabel_cooccurrence(
        self, frame: pd.DataFrame, columns: list[str]
    ) -> pd.DataFrame:
        """Count rows where each pair of sub-labels is jointly positive."""
        if not columns:
            return pd.DataFrame()
        binary = pd.DataFrame(
            {column: frame[column].map(self.consensus_label) for column in columns}
        )
        return binary.T.dot(binary).astype(int)

    def sublabel_profile(
        self, frame: pd.DataFrame, columns: list[str]
    ) -> pd.DataFrame:
        """Profile sub-label positives against consensus toxicity."""
        prepared = self.prepare_frame(frame)
        rows: list[dict[str, int | float | str]] = []
        for column in columns:
            if column not in frame:
                raise KeyError(f"Missing sub-label column: {column}")
            positive = frame[column].map(self.consensus_label).astype(int)
            toxic = prepared[self.label_column].astype(int)
            rows.append(
                {
                    "sublabel": column,
                    "positive_count": int(positive.sum()),
                    "positive_rate": float(positive.mean()),
                    "toxic_positive_count": int(((positive == 1) & (toxic == 1)).sum()),
                    "toxic_positive_rate": float(((positive == 1) & (toxic == 1)).sum() / max((toxic == 1).sum(), 1)),
                    "nontoxic_positive_count": int(((positive == 1) & (toxic == 0)).sum()),
                    "nontoxic_positive_rate": float(((positive == 1) & (toxic == 0)).sum() / max((toxic == 0).sum(), 1)),
                }
            )
        return pd.DataFrame(rows)

    def sublabel_conditioned_rates(
        self,
        frame: pd.DataFrame,
        columns: list[str],
        group_column: str,
    ) -> pd.DataFrame:
        """Report sub-label rates by agreement or topic membership."""
        if group_column == "agreement_band":
            groups = self.annotation_profile(frame)["agreement_band"]
        elif group_column in frame:
            values = frame[group_column].fillna("UNKNOWN").astype(str)
            groups = values.map(
                lambda value: [part.strip() for part in value.split(",") if part.strip()] or ["UNKNOWN"]
            )
        else:
            raise KeyError(f"Missing group column: {group_column}")
        rows: list[dict[str, int | float | str]] = []
        for column in columns:
            positive = frame[column].map(self.consensus_label).astype(int)
            if group_column == "topic":
                pairs = [(topic, index) for index, topics in enumerate(groups) for topic in topics]
            else:
                pairs = [(group, index) for index, group in enumerate(groups)]
            for group, indices in pd.DataFrame(pairs, columns=["group", "index"]).groupby("group")["index"]:
                selected = positive.iloc[indices.tolist()]
                rows.append(
                    {
                        "sublabel": column,
                        "group_column": group_column,
                        "group": group,
                        "count": int(len(selected)),
                        "positive_count": int(selected.sum()),
                        "positive_rate": float(selected.mean()) if len(selected) else 0.0,
                    }
                )
        return pd.DataFrame(rows)

    def sublabel_label_mismatch(
        self, frame: pd.DataFrame, columns: list[str]
    ) -> pd.DataFrame:
        """Count sub-label positives missing from or outside consensus toxicity."""
        prepared = self.prepare_frame(frame)
        toxic = prepared[self.label_column].astype(int)
        rows: list[dict[str, int | str]] = []
        for column in columns:
            positive = frame[column].map(self.consensus_label).astype(int)
            rows.append(
                {
                    "sublabel": column,
                    "positive_sublabel_non_toxic": int(((positive == 1) & (toxic == 0)).sum()),
                    "toxic_without_sublabel": int(((positive == 0) & (toxic == 1)).sum()),
                }
            )
        return pd.DataFrame(rows)

    def duplicate_profile(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Profile exact text duplicates and whether their labels conflict."""
        prepared = self.prepare_frame(frame)
        grouped = prepared.groupby(self.text_column, dropna=False)[self.label_column]
        result = grouped.agg(
            duplicate_count="size",
            labels=lambda values: tuple(sorted(set(int(value) for value in values))),
        ).reset_index()
        result["label_conflict"] = result["labels"].map(lambda labels: len(labels) > 1)
        return result[result["duplicate_count"] > 1].reset_index(drop=True)

    def marker_profile(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Measure raw social-text markers per row without cleaning them."""
        if self.text_column not in frame:
            raise KeyError(f"Missing text column: {self.text_column}")
        result = self.prepare_frame(frame)
        text = result[self.text_column].fillna("").astype(str)
        letters = text.str.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]").str.len()
        uppercase = text.str.findall(r"[A-ZÀ-ÖØ-Þ]").str.len()
        result["has_url"] = text.str.contains(r"https?://|www\.", regex=True)
        result["has_mention"] = text.str.contains(r"@\w+", regex=True)
        result["has_hashtag"] = text.str.contains(r"#\w+", regex=True)
        result["has_exclamation"] = text.str.contains("!")
        result["has_question"] = text.str.contains(r"\?", regex=True)
        result["has_emoji_or_symbol"] = text.str.contains(r"[^\w\s]", regex=True)
        result["has_repeated_character"] = text.map(
            lambda value: bool(re.search(r"(.)\1{2,}", value))
        )
        result["uppercase_ratio"] = uppercase / letters.replace(0, pd.NA)
        return result

    def marker_detail_profile(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Measure punctuation runs, density, case, and symbol markers."""
        result = self.marker_profile(frame)
        text = result[self.text_column].fillna("").astype(str)
        result["question_count"] = text.str.count(r"\?")
        result["exclamation_count"] = text.str.count("!")
        result["question_run_max"] = text.map(
            lambda value: max((len(match.group()) for match in re.finditer(r"\?+", value)), default=0)
        )
        result["exclamation_run_max"] = text.map(
            lambda value: max((len(match.group()) for match in re.finditer(r"!+", value)), default=0)
        )
        result["has_question_exclamation"] = text.str.contains(r"\?!", regex=True)
        result["has_exclamation_question"] = text.str.contains(r"!\?", regex=True)
        result["punctuation_count"] = text.str.count(r"[!?,.;:]")
        result["punctuation_density"] = result["punctuation_count"] / text.str.len().replace(0, pd.NA)
        result["emoji_or_symbol_count"] = text.map(
            lambda value: sum(not char.isalnum() and not char.isspace() and char not in "!?.,;:" for char in value)
        )
        return result

    def marker_conditioned_rates(
        self, frame: pd.DataFrame, marker: str, group_column: str
    ) -> pd.DataFrame:
        """Report marker presence/count rates by label, agreement, or topic."""
        detailed = self.marker_detail_profile(frame)
        if marker not in detailed:
            raise KeyError(f"Missing marker column: {marker}")
        if group_column == "label":
            groups: list[list[tuple[str, int]]] = [
                [(str(label), index) for index, label in enumerate(detailed[self.label_column])]
            ][0]
        elif group_column == "agreement_band":
            bands = self.annotation_profile(frame)["agreement_band"]
            groups = [(str(band), index) for index, band in enumerate(bands)]
        elif group_column == "topic":
            values = frame["topic"].fillna("UNKNOWN").astype(str)
            groups = [
                (topic.strip() or "UNKNOWN", index)
                for index, value in enumerate(values)
                for topic in value.split(",")
            ]
        else:
            raise KeyError(f"Unsupported group column: {group_column}")
        rows: list[dict[str, int | float | str]] = []
        grouped = pd.DataFrame(groups, columns=["group", "index"]).groupby("group")["index"]
        for group, indices in grouped:
            selected = detailed.iloc[indices.tolist()]
            marker_values = selected[marker]
            marker_count = int(marker_values.sum()) if marker_values.dtype == bool else int((marker_values > 0).sum())
            rows.append(
                {
                    "marker": marker,
                    "group_column": group_column,
                    "group": group,
                    "count": int(len(selected)),
                    "marker_count": marker_count,
                    "marker_rate": marker_count / len(selected) if len(selected) else 0.0,
                }
            )
        return pd.DataFrame(rows)

    def variant_comparison(
        self,
        frame: pd.DataFrame,
        variants: dict[str, Callable[[str], str]],
    ) -> pd.DataFrame:
        """Compare raw text with named transformations using token retention."""
        if self.text_column not in frame:
            raise KeyError(f"Missing text column: {self.text_column}")
        raw = frame[self.text_column].fillna("").astype(str).tolist()
        transformations = {"raw": lambda text: text, **variants}
        raw_tokens = [token for text in raw for token in self.tokens(text)]
        raw_vocab = set(raw_tokens)
        rows: list[dict[str, int | float | str]] = []
        for name, transform in transformations.items():
            transformed = [transform(text) for text in raw]
            tokens = [token for text in transformed for token in self.tokens(text)]
            vocabulary = set(tokens)
            rows.append(
                {
                    "variant": name,
                    "document_count": len(transformed),
                    "token_count": len(tokens),
                    "vocabulary_size": len(vocabulary),
                    "token_retention": len(tokens) / len(raw_tokens) if raw_tokens else 0.0,
                    "raw_vocabulary_overlap": len(vocabulary & raw_vocab) / len(raw_vocab)
                    if raw_vocab else 0.0,
                }
            )
        return pd.DataFrame(rows)

    def variant_comparison_by_group(
        self,
        frame: pd.DataFrame,
        group_columns: list[str],
        variants: dict[str, Callable[[str], str]],
        combine: bool = False,
    ) -> pd.DataFrame:
        """Compare text variants independently inside requested subgroups."""
        if not group_columns:
            raise ValueError("group_columns must not be empty")
        prepared = self.prepare_frame(frame)
        if "agreement_band" in group_columns:
            if self.votes_column not in frame:
                raise KeyError(f"Missing votes column: {self.votes_column}")
            prepared["agreement_band"] = self.annotation_profile(frame)["agreement_band"]
        for column in group_columns:
            if column not in prepared:
                raise KeyError(f"Missing group column: {column}")

        rows: list[dict[str, int | float | str]] = []
        transformations = {"raw": lambda text: text, **variants}
        grouping_sets = [group_columns]
        if not combine:
            grouping_sets = [[column] for column in group_columns]
        for selected_columns in grouping_sets:
            group_frame = prepared[selected_columns].fillna("UNKNOWN").astype(str)
            grouping_key = (
                selected_columns[0]
                if len(selected_columns) == 1
                else selected_columns
            )
            grouped = group_frame.groupby(grouping_key, dropna=False).groups
            group_name = "__".join(selected_columns)
            for group_values, indices in grouped.items():
                if not isinstance(group_values, tuple):
                    group_values = (group_values,)
                subset = prepared.loc[indices, self.text_column]
                raw = subset.fillna("").astype(str).tolist()
                raw_tokens = [token for text in raw for token in self.tokens(text)]
                raw_vocabulary = set(raw_tokens)
                for variant, transform in transformations.items():
                    transformed = [transform(text) for text in raw]
                    tokens = [token for text in transformed for token in self.tokens(text)]
                    vocabulary = set(tokens)
                    rows.append(
                        {
                            "group_column": group_name,
                            "group": "|".join(map(str, group_values)),
                            "variant": variant,
                            "document_count": len(transformed),
                            "token_count": len(tokens),
                            "vocabulary_size": len(vocabulary),
                            "token_retention": len(tokens) / len(raw_tokens)
                            if raw_tokens else 0.0,
                            "raw_vocabulary_overlap": len(vocabulary & raw_vocabulary)
                            / len(raw_vocabulary) if raw_vocabulary else 0.0,
                        }
                    )
        return pd.DataFrame(rows)

    def variant_marker_retention(
        self,
        frame: pd.DataFrame,
        variants: dict[str, Callable[[str], str]],
    ) -> pd.DataFrame:
        """Compare marker rates before and after each text transformation."""
        raw = self.marker_profile(frame)
        raw_rates = raw.mean(numeric_only=True)
        rows: list[dict[str, int | float | str]] = []
        transformations = {"raw": lambda text: text, **variants}
        for name, transform in transformations.items():
            transformed = frame.copy(deep=True)
            transformed[self.text_column] = (
                transformed[self.text_column].fillna("").astype(str).map(transform)
            )
            profile = self.marker_profile(transformed)
            row: dict[str, int | float | str] = {"variant": name}
            for column in raw.columns:
                if column in profile and pd.api.types.is_numeric_dtype(profile[column]):
                    value = profile[column].mean()
                    baseline = raw_rates.get(column, 0.0)
                    row[column + "_rate"] = float(value)
                    row["raw_" + column + "_rate"] = float(baseline)
                    row[column + "_delta"] = float(value - baseline)
            rows.append(row)
        return pd.DataFrame(rows)

    def variant_signal_ablation(
        self,
        frame: pd.DataFrame,
        variants: dict[str, Callable[[str], str]],
        top_n: int = 20,
        min_count: int = 1,
    ) -> pd.DataFrame:
        """Measure whether each text variant preserves the toxic/non-toxic signal.

        For every variant (plus an identity ``raw`` baseline), the method
        recomputes document-presence log-odds and compares the top-N
        discriminating tokens against the raw baseline using Jaccard overlap.
        Vocabulary size and raw-vocabulary overlap are also reported so a
        collapse from leet/slang normalization is distinguishable from a loss
        of signal.
        """
        if top_n < 1:
            raise ValueError("top_n must be at least 1")
        if min_count < 1:
            raise ValueError("min_count must be at least 1")
        if self.text_column not in frame:
            raise KeyError(f"Missing text column: {self.text_column}")

        transformations = {"raw": lambda text: text, **variants}
        raw_text = frame[self.text_column].fillna("").astype(str).tolist()
        raw_vocabulary = {token for text in raw_text for token in self.tokens(text)}

        raw_lexical = self.lexical_log_odds(frame, subset="all", min_count=min_count)
        raw_toxic_top = self._top_discriminating(raw_lexical, label=1, top_n=top_n)
        raw_nontoxic_top = self._top_discriminating(raw_lexical, label=0, top_n=top_n)

        rows: list[dict[str, int | float | str]] = []
        for name, transform in transformations.items():
            transformed = frame.copy(deep=True)
            transformed[self.text_column] = transformed[self.text_column].fillna(
                ""
            ).astype(str).map(transform)
            lexical = self.lexical_log_odds(
                transformed, subset="all", min_count=min_count
            )
            vocabulary = {
                token
                for text in transformed[self.text_column]
                for token in self.tokens(text)
            }
            rows.append(
                {
                    "variant": name,
                    "vocabulary_size": len(vocabulary),
                    "raw_vocabulary_overlap": len(vocabulary & raw_vocabulary)
                    / len(raw_vocabulary)
                    if raw_vocabulary
                    else 0.0,
                    "toxic_top_overlap": self._jaccard(
                        raw_toxic_top,
                        self._top_discriminating(lexical, label=1, top_n=top_n),
                    ),
                    "nontoxic_top_overlap": self._jaccard(
                        raw_nontoxic_top,
                        self._top_discriminating(lexical, label=0, top_n=top_n),
                    ),
                }
            )
        return pd.DataFrame(rows)

    @staticmethod
    def _top_discriminating(
        lexical: pd.DataFrame, label: int, top_n: int
    ) -> set[str]:
        """Return top-N tokens for one label ordered by descending log-odds."""
        subset = lexical.loc[lexical["label"] == label]
        return set(subset.sort_values("log_odds", ascending=False)["token"].head(top_n))

    @staticmethod
    def _jaccard(left: set[str], right: set[str]) -> float:
        """Return Jaccard similarity, treating two empty sets as identical."""
        union = left | right
        if not union:
            return 1.0
        return len(left & right) / len(union)

    def topic_membership_rates(
        self, frame: pd.DataFrame, topic_column: str = "topic"
    ) -> pd.DataFrame:
        """Calculate label rates by membership in comma-separated topics."""
        prepared = self.prepare_frame(frame)
        if topic_column not in prepared:
            raise KeyError(f"Missing topic column: {topic_column}")
        memberships = prepared[topic_column].fillna("UNKNOWN").astype(str).map(
            lambda value: [part.strip() for part in value.split(",") if part.strip()]
            or ["UNKNOWN"]
        )
        rows: list[dict[str, int | str]] = []
        for label, topics in zip(prepared[self.label_column], memberships):
            rows.extend({"topic": topic, "label": int(label)} for topic in topics)
        expanded = pd.DataFrame(rows)
        grouped = expanded.groupby("topic")["label"]
        result = grouped.agg(count="size", toxic_count="sum").reset_index()
        result["toxic_rate"] = result["toxic_count"] / result["count"]
        return result.sort_values("topic").reset_index(drop=True)

    def lexical_log_odds(
        self,
        frame: pd.DataFrame,
        subset: str = "all",
        min_count: int = 2,
        smoothing: float = 0.5,
    ) -> pd.DataFrame:
        """Compare document-presence log-odds for tokens across labels.

        ``subset`` separates all, unanimous, and borderline annotation rows.
        Smoothing prevents zero-count divisions and does not alter input data.
        """
        if subset not in {"all", "unanimous", "borderline"}:
            raise ValueError("subset must be all, unanimous, or borderline")
        if min_count < 1:
            raise ValueError("min_count must be at least 1")
        if smoothing <= 0:
            raise ValueError("smoothing must be positive")
        prepared = self.prepare_frame(frame)
        if subset != "all":
            if self.votes_column not in frame:
                raise KeyError(f"Missing votes column: {self.votes_column}")
            bands = self.annotation_profile(frame)["agreement_band"]
            prepared = prepared.loc[bands == subset].copy()

        class_sizes = prepared[self.label_column].value_counts().to_dict()
        document_counts: dict[int, Counter[str]] = {0: Counter(), 1: Counter()}
        for label, values in zip(prepared[self.label_column], prepared["tokens"]):
            document_counts[int(label)].update(set(values))
        vocabulary = sorted(set(document_counts[0]) | set(document_counts[1]))
        rows: list[dict[str, int | float | str]] = []
        for token in vocabulary:
            counts = {label: document_counts[label][token] for label in (0, 1)}
            if max(counts.values()) < min_count:
                continue
            odds = {
                label: (counts[label] + smoothing)
                / (class_sizes.get(label, 0) - counts[label] + smoothing)
                for label in (0, 1)
            }
            for label in (0, 1):
                other = 1 - label
                rows.append(
                    {
                        "subset": subset,
                        "token": token,
                        "label": label,
                        "document_count": counts[label],
                        "document_rate": counts[label] / class_sizes.get(label, 1),
                        "log_odds": float(math.log(odds[label] / odds[other])),
                    }
                )
        return pd.DataFrame(rows).sort_values(
            ["log_odds", "token"], ascending=[False, True]
        ).reset_index(drop=True)

    def ngram_by_group(
        self,
        frame: pd.DataFrame,
        group_column: str,
        n: int = 2,
        min_count: int = 2,
    ) -> pd.DataFrame:
        """Compare n-gram document rates by label inside each group."""
        if n < 1:
            raise ValueError("n must be at least 1")
        if min_count < 1:
            raise ValueError("min_count must be at least 1")
        prepared = self.prepare_frame(frame)
        if group_column not in prepared:
            raise KeyError(f"Missing group column: {group_column}")
        groups = prepared[group_column].fillna("UNKNOWN").astype(str)
        rows: list[dict[str, int | float | str]] = []
        for group in sorted(groups.unique()):
            subset = prepared.loc[groups == group]
            class_sizes = subset[self.label_column].value_counts().to_dict()
            ngrams_by_label: dict[int, Counter[str]] = {0: Counter(), 1: Counter()}
            for label, tokens in zip(subset[self.label_column], subset["tokens"]):
                ngrams = {" ".join(value) for value in zip(*(tokens[i:] for i in range(n)))}
                ngrams_by_label[int(label)].update(ngrams)
            vocabulary = sorted(set(ngrams_by_label[0]) | set(ngrams_by_label[1]))
            for ngram in vocabulary:
                counts = {label: ngrams_by_label[label][ngram] for label in (0, 1)}
                if max(counts.values()) < min_count:
                    continue
                rows.append(
                    {
                        "group": group,
                        "ngram": ngram,
                        "n": n,
                        "nontoxic_document_count": counts[0],
                        "toxic_document_count": counts[1],
                        "nontoxic_document_rate": counts[0] / class_sizes.get(0, 1),
                        "toxic_document_rate": counts[1] / class_sizes.get(1, 1),
                    }
                )
        return pd.DataFrame(rows).sort_values(
            ["group", "toxic_document_rate", "ngram"],
            ascending=[True, False, True],
        ).reset_index(drop=True)

    def kwic_by_group(
        self,
        frame: pd.DataFrame,
        term: str,
        group_column: str,
        window: int = 3,
    ) -> pd.DataFrame:
        """Return keyword-in-context evidence with group and label metadata."""
        if window < 0:
            raise ValueError("window must be non-negative")
        prepared = self.prepare_frame(frame)
        if group_column not in prepared:
            raise KeyError(f"Missing group column: {group_column}")
        groups = prepared[group_column].fillna("UNKNOWN").astype(str)
        target = term.lower()
        rows: list[dict[str, Any]] = []
        texts = prepared[self.text_column].tolist()
        labels = prepared[self.label_column].tolist()
        token_rows = prepared["tokens"].tolist()
        for group, text, label, tokens in zip(groups.tolist(), texts, labels, token_rows):
            for position, token in enumerate(tokens):
                if token == target:
                    rows.append(
                        {
                            "group": group,
                            "text": text,
                            "label": int(label),
                            "position": position,
                            "left_context": " ".join(tokens[max(0, position - window):position]),
                            "term": token,
                            "right_context": " ".join(tokens[position + 1:position + 1 + window]),
                        }
                    )
        return pd.DataFrame(rows)

    @classmethod
    def tokens(cls, text: str) -> list[str]:
        """Tokenize text for descriptive EDA only; raw text remains unchanged."""
        return [token.lower() for token in cls.TOKEN_PATTERN.findall(text)]

    @staticmethod
    def _agreement_ratio(votes: list[int]) -> float:
        """Return majority agreement ratio for parsed binary votes."""
        if not votes:
            return float("nan")
        positives = sum(votes)
        negatives = len(votes) - positives
        return max(positives, negatives) / len(votes)

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
