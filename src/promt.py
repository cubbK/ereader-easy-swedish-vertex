from vertexai.generative_models import GenerativeModel, SafetySetting


def promt_it(
    text: str,
    model_name: str = "gemini-1.5-pro-002",
    generation_config: dict[str, float] = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    },
):
    model = GenerativeModel(
        model_name,
    )

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

    chat = model.start_chat()

    message = chat.send_message(
        [text],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return message
