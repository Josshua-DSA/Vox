"""
Shared test fixtures for IndoToxic test suite.
"""

import numpy as np
import pytest
from sqlalchemy import delete

from src.database.connection import engine, init_db
from src.database.models import RawScrape
from src.evaluation.metrics import MetricCalculator
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import SlangNormalizer
from src.preprocessing.padder import SequencePadder
from src.preprocessing.stopword_filter import StopwordFilter
from src.preprocessing.tokenizer import TextTokenizer

# ─── Database ───────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def db_init():
    """Inisialisasi skema database sekali untuk seluruh test session."""
    init_db()


TEST_SOURCES = ("twitter_test", "forum_test", "youtube_test")


@pytest.fixture(autouse=True)
def clean_test_scrapes():
    """Hapus baris test raw_scrapes sebelum & sesudah tiap test (hermetic)."""
    stmt = delete(RawScrape).where(RawScrape.source.in_(TEST_SOURCES))
    with engine.begin() as conn:
        conn.execute(stmt)
    yield
    with engine.begin() as conn:
        conn.execute(stmt)


# ─── Preprocessing ──────────────────────────────────────────

@pytest.fixture
def cleaner():
    """Instance TextCleaner."""
    return TextCleaner()


@pytest.fixture(scope="session")
def normalizer():
    """Instance SlangNormalizer (shared, read-only)."""
    return SlangNormalizer()


@pytest.fixture
def stopword_filter():
    """Instance StopwordFilter."""
    return StopwordFilter()


@pytest.fixture
def tokenizer():
    """Instance TextTokenizer dengan vocab kecil untuk test."""
    return TextTokenizer(vocab_size=100)


@pytest.fixture
def padder():
    """Instance SequencePadder dengan max_len=5."""
    return SequencePadder(max_len=5, padding="post", pad_value=0)


# ─── Evaluation ─────────────────────────────────────────────

@pytest.fixture
def metric_calculator():
    """Instance MetricCalculator."""
    return MetricCalculator()


# ─── Sample Data ────────────────────────────────────────────

@pytest.fixture
def sample_corpus():
    """Corpus teks sample untuk tokenizer test."""
    return ["ujaran kebencian dilarang", "kebencian menimbulkan masalah"]


@pytest.fixture
def sample_labels_perfect():
    """Label pair sempurna (100% accuracy)."""
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 1])
    return y_true, y_pred
