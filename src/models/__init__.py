"""
Modul arsitektur model klasifikasi teks: BaseModel, CNNTextClassifier, dan EmbeddingLoader.
"""

from src.models.base_model import BaseModel
from src.models.cnn_model import CNNTextClassifier
from src.models.embedding import EmbeddingLoader

__all__ = ["BaseModel", "CNNTextClassifier", "EmbeddingLoader"]
