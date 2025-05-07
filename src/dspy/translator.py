from typing import Literal
import dspy

lm = dspy.LM("vertex_ai/gemini-2.0-flash-001")
lm_local = dspy.LM(
    "ollama_chat/deepseek-r1:1.5b", api_base="http://localhost:11434", api_key=""
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


if __name__ == "__main__":
    result = translator("Hello, how are you today?")
    print(f"Original: {result.english}")
    print(f"Easy English: {result.easy_english}")
    print(f"Swedish: {result.swedish}")
