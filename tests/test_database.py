"""
Unit test untuk modul database PostgreSQL IndoToxic.
"""

import uuid
import pytest
import pandas as pd
from src.database.connection import init_db
from src.database.repository import DatasetRepository, ScraperRepository


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Pastikan skema database terinisialisasi."""
    init_db()


def test_dataset_repository_counts():
    """Uji total hitungan data yang termigrasi."""
    total_count = DatasetRepository.get_total_count()
    assert total_count == 28445

    counts = DatasetRepository.get_counts_by_split()
    assert "train" in counts
    assert "val" in counts
    assert "test" in counts
    assert counts["train"] == 19911
    assert counts["val"] == 4267
    assert counts["test"] == 4267


def test_dataset_repository_get_by_split():
    """Uji pengambilan subset dataset per split."""
    df_train = DatasetRepository.get_by_split("train")
    assert isinstance(df_train, pd.DataFrame)
    assert len(df_train) == 19911
    assert set(["text_id", "text_clean", "topic", "label", "split"]).issubset(df_train.columns)

    df_test = DatasetRepository.get_by_split("test")
    assert len(df_test) == 4267


def test_scraper_repository_raw_insert_and_retrieve():
    """Uji penyimpanan dan pembacaan raw JSON payload scraping."""
    unique_post_id = f"test_tweet_{uuid.uuid4().hex[:8]}"
    dummy_payload = {
        "text": "uji coba postingan toxic twitter",
        "author": "user123",
        "metrics": {"retweets": 10, "likes": 50}
    }
    scrape_id = ScraperRepository.insert_raw_scrape(
        source="twitter_test",
        raw_payload=dummy_payload,
        source_post_id=unique_post_id
    )
    assert scrape_id > 0

    pending_items = ScraperRepository.get_pending_scrapes(limit=10)
    assert any(item["id"] == scrape_id for item in pending_items)
