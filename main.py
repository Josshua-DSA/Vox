"""
Master CLI Entry Point: Pelatihan, Evaluasi, dan Ekspor Pipeline CNN Hate Speech.
Context-Aware Dual-Input Multi-Kernel CNN.
"""

import argparse
import ast
import os
from pathlib import Path

import pandas as pd

from src.evaluation.confusion import ConfusionMatrixPlotter
from src.evaluation.metrics import MetricCalculator
from src.models.cnn_model import CNNTextClassifier
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import SlangNormalizer
from src.preprocessing.padder import SequencePadder
from src.preprocessing.splitter import DataSplitter
from src.preprocessing.tokenizer import TextTokenizer
from src.preprocessing.topic_encoder import TopicEncoder
from src.training.imbalance import ImbalanceHandler
from src.training.trainer import ModelTrainer
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.seed import set_seed


def _aggregate_votes(value: object) -> int:
    if isinstance(value, str):
        try:
            votes = [int(item) for item in ast.literal_eval(value)]
            return int(bool(votes) and sum(votes) / len(votes) >= 0.5)
        except (ValueError, SyntaxError, TypeError, ZeroDivisionError):
            return 0
    return int(value) if pd.notna(value) else 0


def _agreement_band(value: object) -> str:
    try:
        votes = [int(item) for item in ast.literal_eval(value)]
        ratio = max(sum(votes), len(votes) - sum(votes)) / len(votes)
        return "unanimous" if ratio == 1.0 else "borderline"
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError):
        return "unrated"


def _is_noise(value: object) -> bool:
    if isinstance(value, str):
        try:
            return any(int(item) == 1 for item in ast.literal_eval(value))
        except (ValueError, SyntaxError, TypeError):
            return value.strip().lower() in {"1", "true", "yes"}
    return bool(value)


def run_pipeline(stage: str) -> None:
    """
    Eksekusi tahapan pipeline berdasarkan argumen CLI.

    Args:
        stage: Tahapan ("all", "preprocess", "train", "eval").
    """
    cfg = Config()
    logger = Logger.get_logger("Main")
    set_seed(cfg.SEED)

    logger.info(f"Menjalankan pipeline stage: [{stage}] dengan SEED={cfg.SEED}")

    if stage in ["preprocess", "all"]:
        logger.info("Step 1: Menjalankan Preprocessing & Stratified Splitting...")
        normalizer = SlangNormalizer(config=cfg)
        cleaner = TextCleaner(
            remove_urls=True,
            remove_mentions=True,
            remove_hashtags=True,
            remove_punctuation=False,
            lowercase=True,
            preserve_hashtag_content=True,
            normalizer=normalizer,
        )
        topic_encoder = TopicEncoder(canonical_topics=cfg.CANONICAL_TOPICS)
        splitter = DataSplitter(
            train_ratio=cfg.TRAIN_RATIO,
            val_ratio=cfg.VAL_RATIO,
            test_ratio=cfg.TEST_RATIO,
            seed=cfg.SEED,
        )
        logger.info(
            f"Preprocessing siap: aggregator -> normalizer -> cleaner -> "
            f"topic_encoder ({len(cfg.CANONICAL_TOPICS)} topik)."
        )

        raw_path = Path(cfg.RAW_DATA_CSV)
        frame = pd.read_csv(raw_path)
        frame["label"] = frame["toxicity"].map(_aggregate_votes)
        frame["agreement_band"] = frame["toxicity"].map(_agreement_band)
        frame["text_clean"] = cleaner.clean_batch(frame["text"].astype(str).tolist())
        frame = frame[
            (~frame["is_noise_or_spam_text"].map(_is_noise))
            & (frame["text_clean"].str.len() > 2)
        ].copy()
        for column in (
            "profanity_obscenity",
            "threat_incitement_to_violence",
            "insults",
            "identity_attack",
            "sexually_explicit",
        ):
            if column in frame:
                frame[f"sub_{column}"] = frame[column].map(_aggregate_votes)

        output_columns = [
            "text_id", "text", "text_clean", "topic", "label", "agreement_band",
            *[column for column in frame if column.startswith("sub_")],
        ]
        processed_path = Path(cfg.PROCESSED_DATA_PATH)
        processed_path.parent.mkdir(parents=True, exist_ok=True)
        frame[output_columns].to_csv(processed_path, index=False)

        train_df, val_df, test_df = splitter.split_grouped(frame, group_col="text")
        splitter.save_splits(
            train_df[output_columns],
            val_df[output_columns],
            test_df[output_columns],
            output_dir=cfg.SPLITS_DIR,
        )

        tokenizer = TextTokenizer(
            vocab_size=cfg.VOCAB_SIZE,
            oov_token=cfg.OOV_TOKEN,
            pad_token=cfg.PAD_TOKEN,
        )
        tokenizer.fit(train_df["text_clean"].astype(str).tolist())
        tokenizer_path = Path(cfg.TOKENIZER_OUTPUT)
        tokenizer_path.parent.mkdir(parents=True, exist_ok=True)
        tokenizer.save(str(tokenizer_path))
        topic_encoder.save(cfg.TOPIC_ENCODER_OUTPUT)
        logger.info(
            f"Preprocessing selesai: {len(frame):,} rows, "
            f"group-aware splits dan tokenizer tersimpan."
        )

    if stage in ["train", "all"]:
        logger.info("Step 2: Membangun Context-Aware Dual-Input Multi-Kernel CNN...")
        model_cls = CNNTextClassifier(cfg)
        model_cls.build_model()
        imbalance = ImbalanceHandler(
            strategy=cfg.IMBALANCE_STRATEGY,
            gamma=cfg.FOCAL_GAMMA,
            alpha=cfg.FOCAL_ALPHA,
        )
        trainer = ModelTrainer(model=model_cls, imbalance_handler=imbalance)
        logger.info(f"Model trainer siap dengan strategi imbalance: {cfg.IMBALANCE_STRATEGY}")

        if not os.path.exists(cfg.TRAIN_CSV):
            raise FileNotFoundError("Split belum tersedia; jalankan --stage preprocess terlebih dahulu.")
        tokenizer = TextTokenizer.load(cfg.TOKENIZER_OUTPUT)
        topic_encoder = TopicEncoder.load(cfg.TOPIC_ENCODER_OUTPUT)
        padder = SequencePadder(max_len=cfg.MAX_LEN, padding="post", truncating="post")

        def inputs(frame: pd.DataFrame) -> tuple[object, object]:
            sequences = tokenizer.texts_to_sequences(frame["text_clean"].astype(str).tolist())
            text = padder.pad(sequences)
            topic = topic_encoder.transform(frame["topic"]).reshape(-1, 1)
            return text, topic

        train_df = pd.read_csv(cfg.TRAIN_CSV)
        val_df = pd.read_csv(cfg.VAL_CSV)
        x_train, topic_train = inputs(train_df)
        x_val, topic_val = inputs(val_df)
        trainer.fit(
            X_text_train=x_train,
            X_topic_train=topic_train,
            y_train=train_df["label"].to_numpy(),
            X_text_val=x_val,
            X_topic_val=topic_val,
            y_val=val_df["label"].to_numpy(),
        )
        model_cls.save(cfg.MODEL_OUTPUT)
        logger.info(f"Model tersimpan di {cfg.MODEL_OUTPUT}")

    if stage in ["eval", "all"]:
        logger.info("Step 3: Menjalankan Evaluasi & Visualisasi...")
        calculator = MetricCalculator()
        plotter = ConfusionMatrixPlotter()
        logger.info("Evaluator siap.")


def main() -> None:
    """Entry point argparser CLI."""
    parser = argparse.ArgumentParser(
        description="Kelompok 4: Indonesian Hate Speech Detection (Context-Aware Dual-Input CNN)"
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=["all", "preprocess", "train", "eval"],
        help="Tahapan pipeline yang akan dijalankan.",
    )
    args = parser.parse_args()
    run_pipeline(args.stage)


if __name__ == "__main__":
    main()
