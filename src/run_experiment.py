from src.log_to_bigquery import log_to_bigquery
from src.promt import promt_it
from textstat import textstat
import re


def load_prompt(
    prompt_name: str, input_text: str, previous_text: str, after_text: str
) -> str:
    with open(f"prompts/{prompt_name}.txt", "r") as f:
        template = f.read()

    template = template.replace("{original_chunk}", input_text)
    template = template.replace("{previous_text}", previous_text)
    template = template.replace("{after_text}", after_text)

    return template


def get_readability_score(text):
    textstat.set_lang("sv")
    return textstat.flesch_reading_ease(text)


def run_experiment(
    prompt_names: list[str],
    input_text: str,
    previous_text: str,
    after_text: str,
    test_text: str,
    number_of_iterations: int = 1,
):
    for _ in range(number_of_iterations):
        input_text_last = input_text
        for prompt_name in prompt_names:
            prompt = load_prompt(
                prompt_name, input_text_last, previous_text, after_text
            )

            response = promt_it(prompt)
            input_text_last = response.text

        readability_score_textstat = get_readability_score(input_text_last)

        prompt_test = f"""
        You are an expert Swedish language teacher for learners. Evaluate a candidate translation compared to a reference text.

--- Original Text (English) ---
{input_text}

--- Candidate Translation (LLM Output) ---
{input_text_last}

--- Reference Text (Easy Swedish) ---
{test_text}

Rate the candidate on a scale from 1 to 10 for the following criteria:

1. **Accuracy**: Does it preserve the same meaning as the original English?
2. **Simplicity**: Is it as simple or simpler than the reference?
3. **Clarity**: Would an A1/A2-level Swedish learner understand it?

Return the result in JSON format like this:
{{"accuracy": [1-10],
  "simplicity": [1-10],
  "clarity": [1-10]
}}
        """

        response_test = promt_it(prompt_test)

        json_match = re.search(
            r'\{.*?"accuracy":\s*\d+.*?"simplicity":\s*\d+.*?"clarity":\s*\d+.*?\}',
            response_test.text,
            re.DOTALL,
        )

        score = {
            "readability_score_textstat": readability_score_textstat,
            "json_score": json_match.group(0),  # type: ignore, # type: ignore
            "json_explanation": response_test.text,
        }
        prompt_improve = f"""
            Based on the suggestions from scoring, suggest a better prompt for the translation. if the suggestion is a series of consecutive prompts put them in an array. Keep it generic and not specific to the input text. it should work for any text. Output only the suggestion
            
            Original Text (English):
            {input_text}
            
            Candidate Translation (LLM Output):
            {input_text_last}
            Reference Text (Easy Swedish):
            {test_text}
            
            Scoring and Sugestions:
            {score["json_explanation"]}
        """

        suggestion_prompt = promt_it(prompt_improve)

        log_to_bigquery(
            ", ".join(prompt_names),
            input_text,
            input_text_last,
            suggestion_prompt.text,
            "gemini-1.5-pro-002",
        )
