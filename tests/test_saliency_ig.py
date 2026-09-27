"""Unit tests untuk SaliencyMapper (Integrated Gradients & Leave-One-Out)."""

import pytest

from src.explainability.saliency import SaliencyMapper
from src.models.cnn_model import CNNTextClassifier
from src.preprocessing.padder import SequencePadder
from src.preprocessing.tokenizer import TextTokenizer
from src.utils.config import Config


class TestSaliencyMapper:
    """Pengujian atribusi token via LOO dan Integrated Gradients."""

    @pytest.fixture()
    def setup_pipeline(self):
        cfg = Config()
        tokenizer = TextTokenizer(vocab_size=100)
        corpus = [
            "dasar anjing kamu tidak berguna",
            "kamu sangat pintar dan baik",
            "pemilu 2024 politik damai",
        ]
        tokenizer.fit(corpus)
        padder = SequencePadder(max_len=cfg.MAX_LEN)

        model = CNNTextClassifier(cfg)
        model.build_model()

        mapper = SaliencyMapper(
            model=model, tokenizer=tokenizer, padder=padder, steps=5
        )
        return mapper, cfg

    def test_loo_empty_text(self, setup_pipeline):
        mapper, _ = setup_pipeline
        scores = mapper.compute_leave_one_out("", topic_id=0)
        assert scores == []

    def test_loo_returns_word_scores(self, setup_pipeline):
        mapper, _ = setup_pipeline
        scores = mapper.compute_leave_one_out("dasar anjing kamu", topic_id=0)
        assert len(scores) == 3
        words = [w for w, _ in scores]
        assert words == ["dasar", "anjing", "kamu"]
        for _, s in scores:
            assert isinstance(s, float)
            assert s >= 0.0

    def test_ig_empty_text(self, setup_pipeline):
        mapper, _ = setup_pipeline
        scores = mapper.compute_integrated_gradients("", topic_id=0)
        assert scores == []

    def test_ig_returns_normalized_scores(self, setup_pipeline):
        mapper, _ = setup_pipeline
        scores = mapper.compute_integrated_gradients(
            "dasar anjing kamu", topic_id=0
        )
        assert len(scores) == 3
        for _, s in scores:
            assert isinstance(s, float)
            assert 0.0 <= s <= 1.0
