import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting


class LLM:
    def __init__(self):
        vertexai.init(
            project="dan-ml-learn-6-ffaf",
            location="us-central1",
            api_endpoint="aiplatform.googleapis.com",
        )

    def prompt(
        self,
        text: str,
        model_name: str = "gemini-1.5-pro-002",
        generation_config: dict[str, float] = {},
    ):
        model = GenerativeModel(model_name)

        safety_settings = [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF,
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF,
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF,
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF,
            ),
        ]

        response = model.generate_content(
            text,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        return response.text

    def make_prompt_from_template(
        self,
        prompt_template: str,
        chunk: str,
        previous_chunk: str,
        after_chunk: str,
    ):
        """
        Make a prompt from a template.
        Args:
            prompt_template (str): The template to use for the prompt.
            chunk (str): The chunk of text to insert into the template.
            previous_chunk (str): The previous chunk of text for context.
            after_chunk (str): The chunk of text after the current chunk.
        Returns:
            str: The completed prompt.
        """
        return (
            prompt_template.replace("$CHUNK", chunk)
            .replace("$PREVIOUS_CHUNK", previous_chunk)
            .replace("$AFTER_CHUNK", after_chunk)
        )


prompt_template_1 = """
    I want to translate this part of a book text to swedish. Translate to EASY swedish. Make the sentence structure easy. Make the words easy. Simplify it to A1 level while maintaining the story meaning. output ONLY the translation. Use the previous text to understand the context. previous text: "$PREVIOUS_CHUNK" text to translate: $BEGIN_TEXT$ $CHUNK $END_TEXT$ " DO NOT SKIP ANY TEXT INSIDE $BEGIN_TEXT$ and $END_TEXT$
"""


prompt_template_2 = [
    """
    I want to simplify the text in this book. Translate to EASY english. Make the sentence structure easy. Make the words easy. Simplify it to A1 level while maintaining the story meaning. output ONLY the translation. Use the previous text and after text to understand the context. previous text: "$PREVIOUS_CHUNK" after text: "$AFTER_CHUNK" text to translate: $BEGIN_TEXT$ $CHUNK $END_TEXT$ " DO NOT SKIP ANY TEXT INSIDE $BEGIN_TEXT$ and $END_TEXT$
    """,
    """
    I want to translate to swedish. Translate to EASY swedish. output ONLY the translation. Use the previous text and after text to understand the context. previous text: "$PREVIOUS_CHUNK"  text to translate: $BEGIN_TEXT$ $CHUNK $END_TEXT$ " DO NOT SKIP ANY TEXT INSIDE $BEGIN_TEXT$ and $END_TEXT$
    """,
]


prompt_template_3 = [
    """
    Simplify to a1/a2 english. make the sentence structure easy. use the previous text and after text to understand the context
    previous text: "$PREVIOUS_CHUNK" after text: "$AFTER_CHUNK" text to translate: $BEGIN_TEXT$ $CHUNK $END_TEXT$ " DO NOT SKIP ANY TEXT INSIDE $BEGIN_TEXT$ and $END_TEXT$
    """,
    """
    translate to swedish. Maintain the simple sentence structure. Use the previous text and after text to understand the context. previous text: "$PREVIOUS_CHUNK" after text:  text to translate: $BEGIN_TEXT$ $CHUNK $END_TEXT$ " DO NOT SKIP ANY TEXT INSIDE $BEGIN_TEXT$ and $END_TEXT$
    """,
]
