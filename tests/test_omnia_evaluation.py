# Copyright 2026 OMNIA EYE Corporation.
# SPDX-License-Identifier: Apache-2.0
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from examples.omnia.evaluate import choice_metrics


class EvaluationTests(unittest.TestCase):
    def test_metrics_against_hand_calculation(self):
        rows = [{"id": "1", "expected": "a", "probabilities": {"a": .8, "b": .2}},
                {"id": "2", "expected": "b", "probabilities": {"a": .6, "b": .4}}]
        result = choice_metrics(rows)
        self.assertEqual(result["accuracy"], .5)
        self.assertAlmostEqual(result["brier_multiclass"], .4)
        self.assertAlmostEqual(result["negative_log_likelihood"], -(math.log(.8) + math.log(.4)) / 2)
        self.assertAlmostEqual(result["ece"], .4)
        self.assertEqual(result["coverage"], .5)
        self.assertEqual(result["selective_error_rate"], 0)

    def test_no_acceptance_has_undefined_risk(self):
        result = choice_metrics([{"id": "1", "expected": "a", "probabilities": {"a": .5, "b": .5}}])
        self.assertIsNone(result["selective_error_rate"])
        self.assertEqual(result["coverage"], 0)

    def test_duplicate_labels_and_nonfinite_values_are_rejected(self):
        row = {"id": "same", "expected": "a", "probabilities": {"a": 1., "b": 0.}}
        for rows in ([], [row, row], [{**row, "expected": "unknown"}],
                     [{**row, "probabilities": {"a": float("nan"), "b": 0.}}]):
            with self.assertRaises(ValueError):
                choice_metrics(rows)

    def test_one_confidence_uses_last_bin(self):
        result = choice_metrics([{"id": "1", "expected": "a", "probabilities": {"a": 1., "b": 0.}}])
        self.assertEqual(result["ece"], 0)
        self.assertEqual(result["accuracy"], 1)


if __name__ == "__main__":
    unittest.main()
