import unittest
import numpy as np
from src.evaluation.metrics import MetricCalculator


class TestMetrics(unittest.TestCase):
    """Unit test untuk kalkulasi metrik evaluasi klasifikasi."""

    def setUp(self) -> None:
        self.calculator = MetricCalculator()

    def test_macro_f1_perfect(self) -> None:
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        res = self.calculator.compute_all(y_true, y_pred)
        self.assertEqual(res["macro_f1"], 1.0)
        self.assertEqual(res["accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
