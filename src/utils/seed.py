import random
import numpy as np


def set_seed(seed: int = 42) -> None:
    """
    Set random seed untuk Python, NumPy, dan framework deep learning
    agar semua eksperimen berjalan secara deterministik dan reprodusibel.

    Args:
        seed (int): Nilai integer seed, default 42.
    """
    random.seed(seed)
    np.random.seed(seed)
    try:
        import tensorflow as tf

        tf.random.set_seed(seed)
    except ImportError:
        pass
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
