"""Unit tests untuk Context-Aware Dual-Input CNN dan ImbalanceHandler focal loss."""

import numpy as np
import pytest

from src.models.cnn_model import CNNTextClassifier
from src.training.imbalance import ImbalanceHandler
from src.utils.config import Config


class TestDualInputCNN:
    """Pengujian arsitektur CNN dual-input (teks + topic)."""

    @pytest.fixture()
    def cfg(self):
        return Config()

    @pytest.fixture()
    def model(self, cfg):
        m = CNNTextClassifier(cfg)
        m.build_model()
        return m

    def test_build_model_creates_keras_model(self, model):
        """Model terbangun dan bukan skeleton string."""
        assert model.model is not None
        assert model.model != "TensorFlow_Skeleton_Model"

    def test_model_has_dual_inputs(self, model):
        """Model punya 2 input: text_input dan topic_input."""
        inputs = model.model.inputs
        assert len(inputs) == 2
        input_names = [inp.name for inp in inputs]
        assert any("text" in n for n in input_names)
        assert any("topic" in n for n in input_names)

    def test_model_output_shape(self, model, cfg):
        """Output model (batch, 1) sigmoid."""
        output_shape = model.model.output_shape
        assert output_shape == (None, 1)

    def test_predict_proba_shape(self, model, cfg):
        """predict_proba menghasilkan array (n, 1)."""
        batch = 4
        x_text = np.random.randint(0, cfg.VOCAB_SIZE, (batch, cfg.MAX_LEN))
        x_topic = np.random.randint(0, cfg.NUM_TOPICS, (batch, 1))
        probs = model.predict_proba(x_text, x_topic)
        assert probs.shape == (batch, 1)
        assert np.all(probs >= 0.0) and np.all(probs <= 1.0)

    def test_predict_binary_shape(self, model, cfg):
        """predict menghasilkan array (n,) berisi 0 atau 1."""
        batch = 4
        x_text = np.random.randint(0, cfg.VOCAB_SIZE, (batch, cfg.MAX_LEN))
        x_topic = np.random.randint(0, cfg.NUM_TOPICS, (batch, 1))
        preds = model.predict(x_text, x_topic)
        assert preds.shape == (batch,)
        assert set(preds.tolist()).issubset({0, 1})

    def test_fusion_layer_dimension(self, model, cfg):
        """Layer fusion_vec output = NUM_FILTERS*3 + TOPIC_EMBEDDING_DIM = 416."""
        fusion_layer = None
        for layer in model.model.layers:
            if layer.name == "fusion_vec":
                fusion_layer = layer
                break
        assert fusion_layer is not None
        expected_dim = cfg.NUM_FILTERS * len(cfg.FILTER_SIZES) + cfg.TOPIC_EMBEDDING_DIM
        assert fusion_layer.output.shape[-1] == expected_dim


class TestImbalanceHandlerFocalLoss:
    """Pengujian Binary Focal Loss dan Effective Number Weights."""

    def test_get_binary_focal_loss_returns_callable(self):
        handler = ImbalanceHandler(strategy="focal_loss", gamma=2.0, alpha=0.25)
        loss_fn = handler.get_binary_focal_loss()
        assert callable(loss_fn)
        assert loss_fn.__name__ == "binary_focal_loss"

    def test_focal_loss_none_when_not_focal(self):
        handler = ImbalanceHandler(strategy="class_weight")
        assert handler.get_binary_focal_loss() is None

    def test_focal_loss_computation(self):
        import tensorflow as tf

        handler = ImbalanceHandler(strategy="focal_loss", gamma=2.0, alpha=0.25)
        loss_fn = handler.get_binary_focal_loss()

        y_true = tf.constant([[1.0], [0.0], [1.0]], dtype=tf.float32)
        y_pred = tf.constant([[0.9], [0.1], [0.3]], dtype=tf.float32)
        loss = loss_fn(y_true, y_pred)

        assert float(loss) > 0.0
        assert np.isfinite(float(loss))

    def test_effective_num_weights(self):
        handler = ImbalanceHandler(strategy="focal_loss")
        y = np.array([0, 0, 0, 0, 0, 0, 1, 1])
        weights = handler.compute_effective_num_weights(y, beta=0.999)
        assert 0 in weights and 1 in weights
        # Kelas minoritas (1) harus dapat bobot lebih tinggi
        assert weights[1] > weights[0]

    def test_class_weights_only_on_class_weight_strategy(self):
        handler = ImbalanceHandler(strategy="focal_loss")
        y = np.array([0, 0, 1, 1])
        assert handler.get_class_weights(y) is None

        handler2 = ImbalanceHandler(strategy="class_weight")
        w = handler2.get_class_weights(y)
        assert w is not None
        assert 0 in w and 1 in w
