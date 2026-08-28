"""
Database connection, engine, and session management using SQLAlchemy.
"""

import os
from contextlib import contextmanager
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database.models import Base

# Load environment variables
load_dotenv()

DEFAULT_DB_URL = "postgresql://postgres:postgres@localhost:5434/indotoxic"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# Engine initialization
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Inisialisasi tabel di database jika belum ada.
    """
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Hapus semua tabel database (gunakan hati-hati pada testing).
    """
    Base.metadata.drop_all(bind=engine)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager untuk transaksi session database yang aman.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
