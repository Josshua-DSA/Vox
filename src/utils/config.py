from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """
    Konfigurasi terpusat untuk hyperparameter, jalur file, dan opsi eksperimen.
    """

    # Reproducibility
    SEED: int = 42

    # File Paths
    RAW_DATA_CSV: str = "data/raw/indotoxic2024_annotated_data_v2_final.csv"
    RAW_DEMOGRAPHIC_CSV: str = "data/raw/indotoxic2024_annotator_demographic_data_v2_final.csv"
    PROCESSED_DATA_PATH: str = "data/processed/cleaned_dataset.csv"
    SPLITS_DIR: str = "data/splits/"
    TRAIN_CSV: str = "data/splits/train.csv"
    VAL_CSV: str = "data/splits/val.csv"
    TEST_CSV: str = "data/splits/test.csv"

    # Data Split Ratios
    TRAIN_RATIO: float = 0.70
    VAL_RATIO: float = 0.15
    TEST_RATIO: float = 0.15

    # Preprocessing
    MAX_LEN: int = 128
    VOCAB_SIZE: int = 20000
    OOV_TOKEN: str = "<OOV>"
    PAD_TOKEN: str = "<PAD>"

    # Embedding
    EMBEDDING_DIM: int = 128
    USE_PRETRAINED: bool = False
    PRETRAINED_PATH: str = ""

    # CNN Architecture (Yoon Kim Multi-kernel)
    FILTER_SIZES: List[int] = field(default_factory=lambda: [3, 4, 5])
    NUM_FILTERS: int = 128
    DROPOUT_RATE: float = 0.5
    DENSE_UNITS: int = 128

    # Training Hyperparameters
    BATCH_SIZE: int = 32
    EPOCHS: int = 20
    LEARNING_RATE: float = 1e-3
    EARLY_STOPPING_PATIENCE: int = 5

    # Imbalance Strategy: "none" | "class_weight" | "focal_loss" | "oversample"
    IMBALANCE_STRATEGY: str = "class_weight"
    FOCAL_GAMMA: float = 2.0
    FOCAL_ALPHA: float = 0.25

    # Output Artifacts
    MODEL_OUTPUT: str = "outputs/models/cnn_model.h5"
    TOKENIZER_OUTPUT: str = "outputs/tokenizer/tokenizer.pkl"
    METRICS_OUTPUT_DIR: str = "outputs/metrics/"
    PLOTS_OUTPUT_DIR: str = "outputs/plots/"
