"""
Database Repository layer for IndoToxic dataset and future scraping operations.
"""

from typing import List, Optional, Dict, Any, cast
import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from src.database.connection import get_db_session, engine
from src.database.models import DatasetText, RawScrape


class DatasetRepository:
    """
    Menyediakan operasi query, insert batch, dan ekstraksi data untuk pipeline ML.
    """

    @staticmethod
    def bulk_upsert_texts(records: List[Dict[str, Any]], batch_size: int = 1000) -> int:
        """
        Melakukan bulk upsert data teks ke dataset_texts.
        """
        if not records:
            return 0

        total_inserted = 0
        with get_db_session() as session:
            for i in range(0, len(records), batch_size):
                chunk = records[i:i + batch_size]
                stmt = insert(DatasetText).values(chunk)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["text_id"],
                    set_={
                        "text_clean": stmt.excluded.text_clean,
                        "topic": stmt.excluded.topic,
                        "label": stmt.excluded.label,
                        "split": stmt.excluded.split,
                    }
                )
                session.execute(stmt)
                total_inserted += len(chunk)
        return total_inserted

    @staticmethod
    def get_by_split(split: str) -> pd.DataFrame:
        """
        Mengambil dataset berdasarkan split ('train', 'val', 'test', 'unassigned') sebagai Pandas DataFrame.
        """
        query = select(
            DatasetText.text_id,
            DatasetText.text_clean,
            DatasetText.topic,
            DatasetText.label,
            DatasetText.split
        ).where(DatasetText.split == split)

        return pd.read_sql(query, con=engine)

    @staticmethod
    def get_all() -> pd.DataFrame:
        """
        Mengambil seluruh dataset sebagai Pandas DataFrame.
        """
        query = select(
            DatasetText.text_id,
            DatasetText.text_clean,
            DatasetText.topic,
            DatasetText.label,
            DatasetText.split
        )
        return pd.read_sql(query, con=engine)

    @staticmethod
    def get_counts_by_split() -> Dict[str, int]:
        """
        Menghitung total baris per split data.
        """
        with get_db_session() as session:
            stmt = select(DatasetText.split, func.count(DatasetText.text_id)).group_by(DatasetText.split)
            result = session.execute(stmt).all()
            return {row[0]: row[1] for row in result}

    @staticmethod
    def get_total_count() -> int:
        """
        Menghitung total baris data di dataset_texts.
        """
        with get_db_session() as session:
            stmt = select(func.count(DatasetText.text_id))
            return session.scalar(stmt) or 0


class ScraperRepository:
    """
    Menyediakan operasi penyimpanan dan pelacakan raw payload auto-scraping.
    """

    @staticmethod
    def insert_raw_scrape(source: str, raw_payload: Dict[str, Any], source_post_id: Optional[str] = None) -> int:
        """
        Menyimpan satu raw response hasil scraping JSON ke database.
        """
        with get_db_session() as session:
            record = RawScrape(
                source=source,
                source_post_id=source_post_id,
                raw_payload=raw_payload,
                status="PENDING"
            )
            session.add(record)
            session.flush()
            return cast(int, record.id)

    @staticmethod
    def get_pending_scrapes(limit: int = 100) -> List[Dict[str, Any]]:
        """
        Mengambil antrian scraping dengan status PENDING untuk dibersihkan/dianalisis.
        """
        with get_db_session() as session:
            stmt = select(
                RawScrape.id,
                RawScrape.source,
                RawScrape.source_post_id,
                RawScrape.raw_payload,
                RawScrape.status,
                RawScrape.scraped_at
            ).where(RawScrape.status == "PENDING").limit(limit)
            rows = session.execute(stmt).all()
            return [
                {
                    "id": row.id,
                    "source": row.source,
                    "source_post_id": row.source_post_id,
                    "raw_payload": row.raw_payload,
                    "status": row.status,
                    "scraped_at": row.scraped_at
                }
                for row in rows
            ]
