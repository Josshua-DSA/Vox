"""Tests for leakage-safe EDA split audit."""

import pandas as pd

from src.eda.split_audit import audit_split, make_group_split


def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "text": ["same", "same", "toxic", "safe", "other", "other"],
            "toxicity": ["[0, 0]", "[1, 1]", "[1, 1]", "[0, 0]", "[0, 0]", "[0, 0]"],
            "topic": ["A", "A", "A", "B", "B", "B"],
        }
    )


def test_group_split_keeps_exact_text_groups_together() -> None:
    result = make_group_split(frame(), seed=42)
    assignments = result.loc[result["text"] == "same", "split"].unique()
    assert len(assignments) == 1
    assert set(result["split"]) == {"train", "val", "test"}


def test_group_split_is_deterministic() -> None:
    left = make_group_split(frame(), seed=42)
    right = make_group_split(frame(), seed=42)
    assert left["split"].tolist() == right["split"].tolist()


def test_audit_reports_cross_split_duplicate_leakage() -> None:
    assigned = frame().assign(split=["train", "val", "train", "test", "test", "test"])
    report = audit_split(assigned)
    assert report["cross_split_duplicate_groups"] == 1
    assert report["cross_split_duplicate_rows"] == 2
    assert report["vocabulary_overlap_train_val"] >= 0.0


def test_audit_preserves_conflicting_duplicate_groups() -> None:
    assigned = make_group_split(frame(), seed=42)
    report = audit_split(assigned)
    assert report["duplicate_groups"] == 2
    assert report["conflicting_duplicate_groups"] == 1
    assert report["row_count"] == len(frame())
