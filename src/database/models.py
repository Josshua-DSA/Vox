"""
SQLAlchemy ORM models for IndoToxic dataset and future scraping pipelines.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RawScrape(Base):
    """
    Tampungan payload raw JSON hasil scraping multi-platform (Twitter, YouTube, TikTok, dll).
    Mendukung skema fleksibel tanpa migrasi berkala.
    """
    __tablename__ = "raw_scrapes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False, index=True)
    source_post_id = Column(String(255), unique=True, nullable=True, index=True)
    raw_payload = Column(JSONB, nullable=False)
    status = Column(String(20), default="PENDING", nullable=False, index=True)
    scraped_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relasi ke data teks terstruktur
    dataset_entries = relationship("DatasetText", back_populates="raw_scrape", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_raw_scrapes_payload_gin", "raw_payload", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<RawScrape(id={self.id}, source='{self.source}', status='{self.status}')>"


class DatasetText(Base):
    """
    Tabel data teks terstruktur untuk Machine Learning dan Streamlit UI.
    """
    __tablename__ = "dataset_texts"

    text_id = Column(String(50), primary_key=True)
    raw_scrape_id = Column(Integer, ForeignKey("raw_scrapes.id", ondelete="SET NULL"), nullable=True)
    text_clean = Column(Text, nullable=False)
    topic = Column(String(100), nullable=True, index=True)
    label = Column(SmallInteger, nullable=False, index=True)
    split = Column(String(20), default="unassigned", nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relasi balik ke sumber mentah scraping
    raw_scrape = relationship("RawScrape", back_populates="dataset_entries")

    __table_args__ = (
        CheckConstraint("label IN (0, 1)", name="chk_dataset_texts_label"),
        CheckConstraint("split IN ('train', 'val', 'test', 'unassigned')", name="chk_dataset_texts_split"),
    )

    def __repr__(self) -> str:
        return f"<DatasetText(text_id='{self.text_id}', label={self.label}, split='{self.split}')>"
