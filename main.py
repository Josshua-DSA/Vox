"""
Master CLI Entry Point: Pelatihan, Evaluasi, dan Ekspor Pipeline CNN Hate Speech.
"""

import argparse
import sys
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.seed import set_seed
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.tokenizer import TextTokenizer
from src.preprocessing.padder import SequencePadder
from src.preprocessing.splitter import DataSplitter
from src.models.cnn_model import CNNTextClassifier
from src.training.trainer import ModelTrainer
from src.training.imbalance import ImbalanceHandler
from src.evaluation.metrics import MetricCalculator
from src.evaluation.confusion import ConfusionMatrixPlotter


def run_pipeline(stage: str) -> None:
    """
    Eksekusi tahapan pipeline berdasarkan argumen CLI.

    Args:
        stage (str): Tahapan ("all", "preprocess", "train", "eval").
    """
    cfg = Config()
    logger = Logger.get_logger("Main")
    set_seed(cfg.SEED)

    logger.info(f"Menjalankan pipeline stage: [{stage}] dengan SEED={cfg.SEED}")

    if stage in ["preprocess", "all"]:
        logger.info("Step 1: Menjalankan Preprocessing & Stratified Splitting...")
        cleaner = TextCleaner()
        splitter = DataSplitter(
            train_ratio=cfg.TRAIN_RATIO,
            val_ratio=cfg.VAL_RATIO,
            test_ratio=cfg.TEST_RATIO,
            seed=cfg.SEED,
        )
        logger.info("Preprocessing step siap.")

    if stage in ["train", "all"]:
        logger.info("Step 2: Membangun Arsitektur Yoon Kim Multi-Kernel CNN...")
        model_cls = CNNTextClassifier(cfg)
        model_cls.build_model()
        imbalance = ImbalanceHandler(strategy=cfg.IMBALANCE_STRATEGY)
        trainer = ModelTrainer(model=model_cls, imbalance_handler=imbalance)
        logger.info(f"Model trainer siap dengan strategi imbalance: {cfg.IMBALANCE_STRATEGY}")

    if stage in ["eval", "all"]:
        logger.info("Step 3: Menjalankan Evaluasi & Visualisasi...")
        calculator = MetricCalculator()
        plotter = ConfusionMatrixPlotter()
        logger.info("Evaluator siap.")


def main() -> None:
    """Entry point argparser CLI."""
    parser = argparse.ArgumentParser(
        description="Kelompok 4: Indonesian Hate Speech Detection (CNN for Text)"
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
