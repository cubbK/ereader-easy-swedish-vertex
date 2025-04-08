import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

vertexai.init(
    project="dan-ml-learn-5-b42c",
    location="us-central1",
    api_endpoint="aiplatform.googleapis.com",
)


def generate():
    model = GenerativeModel(
        "gemini-1.5-pro-002",
    )
    chat = model.start_chat()
    print(
        chat.send_message(
            ["""What did Dan ate today?"""],
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
    )


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

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

generate()
