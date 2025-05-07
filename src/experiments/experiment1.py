import dspy
from google.cloud import aiplatform
from src.dspy.translator import translator
from src.dspy.metric import TranslationMetric
from src.dspy.optimization_miprov2 import optimize_translator


if __name__ == "__main__":
