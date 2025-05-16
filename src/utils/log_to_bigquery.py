from google.cloud import bigquery
from datetime import datetime, timezone

bq_client = bigquery.Client()


def log_to_bigquery(row, table_id: str):
    errors = bq_client.insert_rows_json(table_id, [row])
    print(f"Inserting row into {table_id} at {datetime.now(timezone.utc).isoformat()}")
    if errors:
        print("Error inserting row:", errors)
