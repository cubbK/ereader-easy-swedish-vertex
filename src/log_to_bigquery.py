from google.cloud import bigquery
from datetime import datetime, timezone

bq_client = bigquery.Client()


def log_to_bigquery(
    prompt_version: str,
    input_text: str,
    output_text: str,
    suggestion: str,
    model_used: str,
):
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt_version": prompt_version,
        "input_text": input_text,
        "output_text": output_text,
        "suggestion": suggestion,
        "model_used": model_used,
    }
    errors = bq_client.insert_rows_json("translation_logs.experiments", [row])
    if errors:
        print("Error inserting row:", errors)
