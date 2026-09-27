"""Unit tests untuk TopicEncoder."""

import os
import tempfile

import numpy as np
import pandas as pd

from src.preprocessing.topic_encoder import TopicEncoder


class TestTopicEncoder:
    """Pengujian TopicEncoder mapping kategorikal topik."""

    def test_default_canonical_topics(self):
        enc = TopicEncoder()
        assert len(enc.canonical_topics) == 7
        assert enc.canonical_topics[0] == "Politik"
        assert enc.canonical_topics[-1] == "UNKNOWN"

    def test_transform_single_known(self):
        enc = TopicEncoder()
        assert enc.transform_single("Politik") == 0
        assert enc.transform_single("Agama") == 1
        assert enc.transform_single("UNKNOWN") == 6

    def test_transform_single_unknown_fallback(self):
        enc = TopicEncoder()
        result = enc.transform_single("TopikTidakAda")
        assert result == enc.unknown_id

    def test_transform_single_non_string(self):
        enc = TopicEncoder()
        assert enc.transform_single(None) == enc.unknown_id
        assert enc.transform_single(123) == enc.unknown_id

    def test_transform_series(self):
        enc = TopicEncoder()
        topics = pd.Series(["Politik", "Agama", "TidakAda", "SARA"])
        result = enc.transform(topics)
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.int32
        assert list(result) == [0, 1, enc.unknown_id, 2]

    def test_transform_multi_hot(self):
        enc = TopicEncoder()
        vec = enc.transform_multi_hot(["Politik", "SARA"])
        assert vec.shape == (7,)
        assert vec[0] == 1  # Politik
        assert vec[2] == 1  # SARA
        assert vec.sum() == 2

    def test_inverse_transform(self):
        enc = TopicEncoder()
        assert enc.inverse_transform(0) == "Politik"
        assert enc.inverse_transform(99) == "UNKNOWN"

    def test_save_and_load(self):
        enc = TopicEncoder()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "topic_enc.json")
            enc.save(path)
            assert os.path.exists(path)

            loaded = TopicEncoder.load(path)
            assert loaded.canonical_topics == enc.canonical_topics
            assert loaded.transform_single("Agama") == 1

    def test_fit_is_noop(self):
        enc = TopicEncoder()
        series = pd.Series(["Politik", "Agama"])
        result = enc.fit(series)
        assert result is enc
