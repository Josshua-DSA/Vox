"""
Script migrasi data CSV lokal (data/processed/cleaned_dataset.csv & data/splits/*.csv)
ke database PostgreSQL IndoToxic.
"""

import os
import sys
import pandas as pd
from tqdm import tqdm

# Ensure project root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.connection import init_db
from src.database.repository import DatasetRepository
from src.utils.logger import Logger

logger = Logger.get_logger("migration")


def migrate() -> None:
    """
    Melakukan ekstraksi dari CSV dan load ke PostgreSQL.
    """
    logger.info("Memulai inisialisasi tabel database...")
    init_db()

    train_path = "data/splits/train.csv"
    val_path = "data/splits/val.csv"
    test_path = "data/splits/test.csv"
    cleaned_path = "data/processed/cleaned_dataset.csv"

    # Map split status
    split_map = {}
    if os.path.exists(train_path):
        df_train = pd.read_csv(train_path)
        for tid in df_train["text_id"].dropna():
            split_map[str(tid)] = "train"
    if os.path.exists(val_path):
        df_val = pd.read_csv(val_path)
        for tid in df_val["text_id"].dropna():
            split_map[str(tid)] = "val"
    if os.path.exists(test_path):
        df_test = pd.read_csv(test_path)
        for tid in df_test["text_id"].dropna():
            split_map[str(tid)] = "test"

    logger.info(f"Loaded split mapping: {len(split_map)} entries.")

    logger.info(f"Membaca dataset utama dari {cleaned_path}...")
    df_cleaned = pd.read_csv(cleaned_path)
    logger.info(f"Total baris pada {cleaned_path}: {len(df_cleaned)}")

    records = []
    for row in tqdm(df_cleaned.to_dict(orient="records"), total=len(df_cleaned), desc="Preparing records"):
        tid = str(row["text_id"])
        val_clean = row.get("text_clean")
        text_clean = str(val_clean) if val_clean is not None and not pd.isna(val_clean) else ""
        val_topic = row.get("topic")
        topic = str(val_topic) if val_topic is not None and not pd.isna(val_topic) else "UNKNOWN"
        label = int(row["label"])
        split = split_map.get(tid, "unassigned")

        records.append({
            "text_id": tid,
            "text_clean": text_clean,
            "topic": topic,
            "label": label,
            "split": split
        })

    logger.info("Menyimpan records ke database PostgreSQL via bulk upsert...")
    inserted = DatasetRepository.bulk_upsert_texts(records, batch_size=2000)
    logger.info(f"Migrasi selesai! Total baris tersimpan: {inserted}")

    counts = DatasetRepository.get_counts_by_split()
    logger.info(f"Distribusi data per split di database: {counts}")


if __name__ == "__main__":
    migrate()
