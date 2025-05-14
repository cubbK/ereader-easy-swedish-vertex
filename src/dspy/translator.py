from typing import Literal
import dspy
from google.cloud import aiplatform


aiplatform.init(
    experiment="experiment1", project="dan-ml-learn-6-ffaf", location="us-central1"
)

lm = dspy.LM(
    "vertex_ai/gemini-2.0-flash-001",
    cache=False,
)

dspy.configure(lm=lm)


class EnglishToSwedishTranslator(dspy.Module):
    def __init__(self):
        super().__init__()

        self.english_to_easy = dspy.Predict("english -> easy_english")
        self.easy_to_swedish = dspy.Predict("easy_english -> swedish")

    def forward(self, english):
        easy_english = self.english_to_easy(english=english).easy_english
        swedish = self.easy_to_swedish(easy_english=easy_english).swedish

        # Create a prediction object with attributes instead of returning a dict
        prediction = dspy.Prediction(
            english=english, easy_english=easy_english, swedish=swedish
        )
        return prediction


translator = EnglishToSwedishTranslator()
translator.save("translator_raw.json")


if __name__ == "__main__":
    result = translator("Hello, how are you today?")
    print(f"Original: {result.english}")
    print(f"Easy English: {result.easy_english}")
    print(f"Swedish: {result.swedish}")
