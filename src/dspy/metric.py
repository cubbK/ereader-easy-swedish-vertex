import dspy
from src.dspy.evaluator import TranslationEvaluator
from src.dspy.translator import EnglishToSwedishTranslator


class TranslationMetric:
    """Metric for evaluating translation quality using the TranslationEvaluator."""

    def __init__(self):
        self.evaluator = TranslationEvaluator()

    def __call__(self, example, prediction, trace=None):
        english_text = example.english
        easy_swedish = prediction.swedish

        evaluation = self.evaluator(english=english_text, easy_swedish=easy_swedish)

        # Return score between 0 and 1 for MIPRO optimization
        return evaluation["final_score"] / 100.0
