from src.llm import LLM


class Experiment:
    def __init__(self, chunk: str, previous_chunk: str, after_chunk: str):
        """
        Initialize an Experiment object with the chunk of text and its context.
        Args:
            chunk (str): The chunk of text to experiment with.
            previous_chunk (str): The previous chunk of text for context.
            after_chunk (str): The chunk of text after the current chunk.
        """
        self.chunk = chunk
        self.previous_chunk = previous_chunk
        self.after_chunk = after_chunk
        self.llm = LLM()

    def run(self, prompt_template: str):
        """
        Run the experiment using the chunk of text and its context.
        Returns:
            str: The result of the experiment.
        """

        prompt = self.llm.make_prompt_from_template(
            prompt_template, self.chunk, self.previous_chunk, self.after_chunk
        )

        result = self.llm.prompt(prompt)
        score = self.score(result)

        return result, score

    def score(self, result: str):
        """
        Score the result of the experiment.
        Args:
            result (str): The result of the experiment.
        Returns:
            float: The score of the result.
        """

        prompt = f"""
            You are a language expert evaluating Swedish translations for learners.

            You will be given an English sentence and a Swedish translation. Your job is to evaluate the translation on 3 criteria:

            1. **Sentence structure**: Is the structure simple and clear?
            2. **Vocabulary**: Are the words easy and suitable for A1–A2 level learners?
            3. **Meaning**: Does the translation preserve the meaning of the original text?

            For each category, give a score between 1 and 100. Then give a short explanation and a total score out of 100.

            Format your response like this:

            Structure: X  
            Vocabulary: Y  
            Meaning: Z  
            Explanation: ...  
            Total: T
            
            English: "{self.chunk}"

            Swedish: "{result}"
        """
        score = self.llm.prompt(prompt)
        # Placeholder for scoring logic
        return score
