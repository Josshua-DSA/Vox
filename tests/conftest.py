"""
Shared test fixtures for IndoToxic test suite.
"""

import pytest
import numpy as np
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.tokenizer import TextTokenizer
from src.preprocessing.padder import SequencePadder
from src.evaluation.metrics import MetricCalculator
from src.database.connection import init_db


# ─── Database ───────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def db_init():
    """Inisialisasi skema database sekali untuk seluruh test session."""
    init_db()


# ─── Preprocessing ──────────────────────────────────────────

@pytest.fixture
def cleaner():
    """Instance TextCleaner."""
    return TextCleaner()


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
