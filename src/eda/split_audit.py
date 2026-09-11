"""Leakage-safe, non-destructive split and split-audit utilities."""

from __future__ import annotations

import hashlib
from typing import Any

import pandas as pd

from src.eda.text_eda import TextEDA


def _hash_group(value: str, seed: int) -> int:
    digest = hashlib.sha256(f"{seed}:{value}".encode()).hexdigest()
    return int(digest[:16], 16)


def make_group_split(
    frame: pd.DataFrame,
    seed: int = 42,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
) -> pd.DataFrame:
    """Assign exact-text groups to train/val/test deterministically."""
    if not 0 < train_ratio < 1 or not 0 < val_ratio < 1:
        raise ValueError("split ratios must be between 0 and 1")
    if train_ratio + val_ratio >= 1:
        raise ValueError("train_ratio + val_ratio must be below 1")
    if "text" not in frame:
        raise KeyError("Missing text column: text")
    result = frame.copy(deep=True)
    keys = result["text"].fillna("").astype(str)
    unique = sorted(keys.unique(), key=lambda value: _hash_group(value, seed))
    total = len(unique)
    train_end = max(1, round(total * train_ratio))
    if total >= 3:
        train_end = min(train_end, total - 2)
    val_end = max(train_end + 1, round(total * (train_ratio + val_ratio)))
    if total >= 3:
        val_end = min(val_end, total - 1)
    assignment = {
        key: "train" if index < train_end else "val" if index < val_end else "test"
        for index, key in enumerate(unique)
    }
    result["split"] = keys.map(assignment)
    return result


def _vocabulary(values: pd.Series) -> set[str]:
    eda = TextEDA()
    return {token for value in values.fillna("").astype(str) for token in eda.tokens(value)}


def audit_split(frame: pd.DataFrame) -> dict[str, Any]:
    """Return duplicate leakage, distribution, and vocabulary overlap metrics."""
    required = {"text", "split"}
    missing = required - set(frame.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    data = frame.copy(deep=True)
    if "label" not in data and "toxicity" in data:
        data["label"] = data["toxicity"].map(TextEDA().consensus_label)
    data["_text_key"] = data["text"].fillna("").astype(str)
    grouped = data.groupby("_text_key", dropna=False)
    duplicate_groups = grouped.size()
    conflicts = grouped["label"].nunique() if "label" in data else pd.Series(dtype=int)
    split_counts = grouped["split"].nunique()
    leaked = split_counts[split_counts > 1].index
    split_vocab = {name: _vocabulary(data.loc[data["split"] == name, "text"]) for name in data["split"].unique()}
    result: dict[str, Any] = {
        "row_count": int(len(data)),
        "split_counts": data["split"].value_counts().to_dict(),
        "duplicate_groups": int((duplicate_groups > 1).sum()),
        "duplicate_rows": int(duplicate_groups[duplicate_groups > 1].sum()),
        "conflicting_duplicate_groups": int((conflicts > 1).sum()) if not conflicts.empty else 0,
        "cross_split_duplicate_groups": int(len(leaked)),
        "cross_split_duplicate_rows": int(duplicate_groups.loc[leaked].sum()) if len(leaked) else 0,
    }
    for left, right in (("train", "val"), ("train", "test"), ("val", "test")):
        first = split_vocab.get(left, set())
        second = split_vocab.get(right, set())
        result[f"vocabulary_overlap_{left}_{right}"] = len(first & second) / len(first | second) if first | second else 0.0
    if "label" in data:
        result["label_by_split"] = data.groupby("split")["label"].mean().to_dict()
    return result


__all__ = ["audit_split", "make_group_split"]

