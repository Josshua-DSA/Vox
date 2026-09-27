"""Unit tests untuk AnnotatorAgreementAggregator."""

import pandas as pd
import pytest

from src.preprocessing.agreement import AnnotatorAgreementAggregator


class TestAgreementAggregator:
    """Pengujian majority voting dan Fleiss' Kappa."""

    def test_aggregate_votes_majority_positive(self):
        agg = AnnotatorAgreementAggregator(threshold=0.5)
        label, agreement = agg.aggregate_votes([1, 1, 0])
        assert label == 1
        assert agreement == pytest.approx(2 / 3, abs=0.01)

    def test_aggregate_votes_majority_negative(self):
        agg = AnnotatorAgreementAggregator(threshold=0.5)
        label, agreement = agg.aggregate_votes([0, 0, 0, 1])
        assert label == 0
        assert agreement == pytest.approx(3 / 4, abs=0.01)

    def test_aggregate_votes_exact_threshold(self):
        agg = AnnotatorAgreementAggregator(threshold=0.5)
        label, _ = agg.aggregate_votes([1, 0])
        assert label == 1  # 0.5 >= 0.5

    def test_aggregate_votes_empty(self):
        agg = AnnotatorAgreementAggregator()
        label, agreement = agg.aggregate_votes([])
        assert label == 0
        assert agreement == 0.0

    def test_invalid_threshold(self):
        with pytest.raises(ValueError):
            AnnotatorAgreementAggregator(threshold=0.0)
        with pytest.raises(ValueError):
            AnnotatorAgreementAggregator(threshold=1.5)

    def test_parse_votes_string(self):
        votes = AnnotatorAgreementAggregator._parse_votes("['0', '1', '1']")
        assert votes == [0, 1, 1]

    def test_parse_votes_list(self):
        votes = AnnotatorAgreementAggregator._parse_votes([0, 1, 1])
        assert votes == [0, 1, 1]

    def test_process_dataframe(self):
        df = pd.DataFrame({
            "text_id": ["a", "b", "c"],
            "toxicity": ["['1', '1', '0']", "['0', '0']", "['1', '1']"],
        })
        agg = AnnotatorAgreementAggregator()
        result = agg.process_dataframe(df)
        assert "label" in result.columns
        assert "annotator_agreement" in result.columns
        assert list(result["label"]) == [1, 0, 1]

    def test_compute_dataset_kappa(self):
        df = pd.DataFrame({
            "toxicity": [
                "['1', '1']",
                "['0', '0']",
                "['1', '0']",
                "['0', '0']",
            ]
        })
        agg = AnnotatorAgreementAggregator()
        kappa = agg.compute_dataset_kappa(df)
        # Kappa should be a finite number between -1 and 1
        assert -1.0 <= kappa <= 1.0
