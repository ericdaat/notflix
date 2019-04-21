import unittest
from src.recommender import evaluate_recommendations


class TestMetrics(unittest.TestCase):
    def test_evaluate_recommendations(self):
        target = {"A", "B", "C"}

        s1 = evaluate_recommendations(["X", "Y", "Z", "A", "B"], target, 3)
        s2 = evaluate_recommendations(["Z", "B", "A", "X", "Y"], target, 3)
        s3 = evaluate_recommendations(["A", "B", "Z", "X", "Y"], target, 3)

        self.assertTrue(s1 < s2 < s3)
