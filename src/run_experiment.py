from src.log_to_bigquery import log_to_bigquery
from src.promt import promt_it


def load_prompt(
    prompt_name: str, input_text: str, previous_text: str, after_text: str
) -> str:
    with open(f"prompts/{prompt_name}.txt", "r") as f:
        template = f.read()

    template = template.replace("{original_chunk}", input_text)
    template = template.replace("{previous_text}", previous_text)
    template = template.replace("{after_text}", after_text)

    return template


def run_experiment(
    prompt_names: list[str],
    input_text: str,
    previous_text: str,
    after_text: str,
):
    input_text_last = input_text
    for prompt_name in prompt_names:
        prompt = load_prompt(prompt_name, input_text_last, previous_text, after_text)

        response = promt_it(prompt)
        input_text_last = response.text

    print(f"Prompt Names: {prompt_names}")
    print(f"Input: {input_text}")
    print(f"Output: {input_text_last}")

    log_to_bigquery(
        ", ".join(prompt_names), input_text, input_text_last, "gemini-1.5-pro-002"
    )
