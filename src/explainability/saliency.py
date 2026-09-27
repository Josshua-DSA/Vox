"""
SaliencyMapper: Integrated Gradients (50 steps) dan Leave-One-Out proxy
untuk atribusi tingkat kata pada prediksi CNN dual-input.
Sesuai ARCHITECTURE.md §4.5.
"""

from typing import Any

import numpy as np


class SaliencyMapper:
    """
    Menghitung skor atribusi kontribusi kata terhadap probabilitas prediksi
    model CNN dual-input menggunakan Integrated Gradients dan LOO proxy.

    Attributes:
        model: Objek model CNN (harus punya atribut .model Keras Model).
        tokenizer: Objek TextTokenizer.
        padder: Objek SequencePadder.
        steps: Jumlah langkah interpolasi IG (default 50).
    """

    def __init__(
        self, model: Any, tokenizer: Any, padder: Any, steps: int = 50
    ) -> None:
        """
        Inisialisasi mapper.

        Args:
            model: Objek model CNN dengan .model (Keras) dan .predict_proba().
            tokenizer: Objek TextTokenizer dengan .texts_to_sequences().
            padder: Objek SequencePadder dengan .pad().
            steps: Jumlah interpolation steps untuk IG.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.padder = padder
        self.steps = steps

    def compute_leave_one_out(
        self, text: str, topic_id: int
    ) -> list[tuple[str, float]]:
        """
        Menghitung bobot pentingnya kata via Leave-One-Out proxy.
        delta_p = p_ref - p_{tanpa kata_i}

        Args:
            text: Teks kalimat input.
            topic_id: Integer ID topik.

        Returns:
            List tuple (kata, skor_atribusi).
        """
        words = text.split()
        if not words:
            return []

        base_seq = self.tokenizer.texts_to_sequences([text])
        base_padded = self.padder.pad(base_seq)
        topic_arr = np.array([[topic_id]], dtype=np.int32)
        base_prob = float(self.model.predict_proba(base_padded, topic_arr)[0, 0])

        saliency_scores: list[tuple[str, float]] = []
        for i in range(len(words)):
            sub_words = words[:i] + words[i + 1:]
            if not sub_words:
                saliency_scores.append((words[i], 1.0))
                continue
            sub_text = " ".join(sub_words)
            sub_seq = self.tokenizer.texts_to_sequences([sub_text])
            sub_padded = self.padder.pad(sub_seq)
            sub_prob = float(self.model.predict_proba(sub_padded, topic_arr)[0, 0])

            importance = max(0.0, base_prob - sub_prob)
            saliency_scores.append((words[i], round(importance, 4)))

        return saliency_scores

    def compute_integrated_gradients(
        self, text: str, topic_id: int
    ) -> list[tuple[str, float]]:
        """
        Menghitung Integrated Gradients dari baseline nol ke embedding input.

        IG_i(X) = (x_i - x'_i) * (1/S) * sum dF/dx_i evaluated at interpolated points.

        Falls back to LOO if TensorFlow unavailable or model incompatible.

        Args:
            text: Teks kalimat input.
            topic_id: Integer ID topik.

        Returns:
            List tuple (kata, skor_atribusi_normalized).
        """
        words = text.split()
        if not words:
            return []

        try:
            import tensorflow as tf
        except ImportError:
            return self.compute_leave_one_out(text, topic_id)

        keras_model = getattr(self.model, "model", None)
        if keras_model is None or not hasattr(keras_model, "input"):
            return self.compute_leave_one_out(text, topic_id)

        # Prepare inputs
        seq = self.tokenizer.texts_to_sequences([text])
        padded = self.padder.pad(seq)
        text_ids = tf.constant(padded, dtype=tf.int32)
        topic_ids = tf.constant([[topic_id]], dtype=tf.int32)

        # Find text embedding layer
        emb_layer = None
        for layer in keras_model.layers:
            if "embedding" in layer.name and "topic" not in layer.name:
                emb_layer = layer
                break

        if emb_layer is None:
            return self.compute_leave_one_out(text, topic_id)

        # Get embedding weights for lookup
        input_emb = emb_layer(text_ids)  # (1, max_len, emb_dim)
        baseline_emb = tf.zeros_like(input_emb)

        # Build a sub-model: embedding tensor + topic_input -> output
        # Use GradientTape with a custom forward pass
        accumulated_grads = tf.zeros_like(input_emb, dtype=tf.float32)

        for s in range(1, self.steps + 1):
            alpha = s / self.steps
            interpolated = baseline_emb + alpha * (input_emb - baseline_emb)
            interpolated = tf.cast(interpolated, tf.float32)

            with tf.GradientTape() as tape:
                tape.watch(interpolated)
                # Manual forward: pass interpolated through post-embedding layers
                output = self._forward_from_embedding(
                    keras_model, emb_layer.name, interpolated, topic_ids
                )

            if output is not None:
                grads = tape.gradient(output, interpolated)
                if grads is not None:
                    accumulated_grads = accumulated_grads + grads

        avg_grads = accumulated_grads / float(self.steps)
        ig = (input_emb - baseline_emb) * avg_grads  # (1, max_len, emb_dim)

        token_scores = tf.reduce_sum(tf.abs(ig[0]), axis=-1).numpy()
        n_words = min(len(words), len(token_scores))
        scores = token_scores[:n_words]

        max_score = float(scores.max()) if scores.max() > 0 else 1.0
        normalized = scores / max_score

        return [(words[i], round(float(normalized[i]), 4)) for i in range(n_words)]

    @staticmethod
    def _forward_from_embedding(
        keras_model: Any,
        emb_layer_name: str,
        interpolated_emb: Any,
        topic_ids: Any,
    ) -> Any:
        """
        Manual forward pass from interpolated text embedding through model layers.

        Args:
            keras_model: Keras Functional API model.
            emb_layer_name: Name of text embedding layer.
            interpolated_emb: Interpolated embedding tensor (1, max_len, emb_dim).
            topic_ids: Topic input tensor (1, 1).

        Returns:
            Output tensor or None on failure.
        """

        x = interpolated_emb
        conv_outputs = []
        topic_vec = None
        conv_out = None

        for layer in keras_model.layers:
            name = layer.name

            # Skip input layers and the embedding we replaced
            if name in ("text_input", "topic_input", emb_layer_name):
                continue

            # Topic branch
            if name == "topic_embedding":
                topic_vec = layer(topic_ids)
                continue
            if name == "topic_vec" and topic_vec is not None:
                topic_vec = layer(topic_vec)
                continue

            # Conv1D branches
            if name.startswith("conv1d_k"):
                conv_out = layer(x)
                continue
            if name.startswith("gmp_k") and conv_out is not None:
                pool_out = layer(conv_out)
                conv_outputs.append(pool_out)
                conv_out = None
                continue

            # Text vec concatenation
            if name == "text_vec":
                if len(conv_outputs) > 1:
                    x = layer(conv_outputs)
                elif conv_outputs:
                    x = conv_outputs[0]
                continue

            # Fusion
            if name == "fusion_vec":
                if topic_vec is not None:
                    x = layer([x, topic_vec])
                continue

            # Regular sequential layers (dropout, dense, output)
            try:
                x = layer(x)
            except (ValueError, TypeError):
                return None

        return x
