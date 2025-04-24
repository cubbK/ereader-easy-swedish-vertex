import dspy

lm = dspy.LM("vertex_ai/gemini-1.5-pro-002")
dspy.configure(lm=lm)


class EnglishToSwedishTranslator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.english_to_easy = dspy.Predict("english -> easy_english")
        self.easy_to_swedish = dspy.Predict("easy_english -> swedish")

    def forward(self, english_text):
        easy_english = self.english_to_easy(english=english_text).easy_english
        swedish = self.easy_to_swedish(easy_english=easy_english).swedish
        return {
            "english": english_text,
            "easy_english": easy_english,
            "swedish": swedish,
        }


translator = EnglishToSwedishTranslator()


if __name__ == "__main__":
    result = translator("Hello, how are you today?")
    print(f"Original: {result['english']}")
    print(f"Easy English: {result['easy_english']}")
    print(f"Swedish: {result['swedish']}")
