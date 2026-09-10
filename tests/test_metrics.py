"""Unit test untuk kalkulasi metrik evaluasi klasifikasi."""


class TestMetrics:
    def test_macro_f1_perfect(self, metric_calculator, sample_labels_perfect):
        y_true, y_pred = sample_labels_perfect
        res = metric_calculator.compute_all(y_true, y_pred)
        assert res["macro_f1"] == 1.0
        assert res["accuracy"] == 1.0
