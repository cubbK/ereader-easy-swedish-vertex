from google.cloud import bigquery
from google.cloud import storage
import os
from typing import Optional, Dict, Any


def get_best_score_from_bigquery(
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Fetches the experiment with the best score from BigQuery.

    Args:
        project_id: The BigQuery project ID
        dataset_id: The BigQuery dataset ID
        table_id: The BigQuery table ID

    Returns:
        A dictionary containing the best experiment information (highest score)
        or None if no experiments found
    """
    client = bigquery.Client()

    query = f"""
    SELECT 
        experiment_id,
        score,
        inserted_at
    FROM 
        `{project_id}.{dataset_id}.{table_id}`
    WHERE 
        score IS NOT NULL
    ORDER BY 
        score DESC
    LIMIT 1
    """

    try:
        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            return {
                "experiment_id": row.experiment_id,
                "score": row.score,
                "inserted_at": row.inserted_at,
            }

        return None
    except Exception as e:
        print(f"Error retrieving best score from BigQuery: {e}")
        return None


def upgrade_best_prompt(
    project_id: str,
    dataset_id: str,
    table_id: str,
    source_bucket_name: str = "dan-ml-learn-6-ffaf-experiments",
    destination_bucket_name: str = "dan-ml-learn-6-ffaf-experiments",
    destination_blob_name: str = "experiment1/best_prompt_latest.json",
) -> Optional[Dict[str, Any]]:
    """
    Upgrades the best prompt based on the highest score from BigQuery.
    Copies the file from source to destination with a new name.

    Args:
        project_id: The BigQuery project ID
        dataset_id: The BigQuery dataset ID
        table_id: The BigQuery table ID
        source_bucket_name: The GCS bucket containing the source file
        destination_bucket_name: The GCS bucket for the destination file
        destination_blob_name: The new name for the copied file

    Returns:
        A dictionary containing the best experiment information or None if failed
    """
    best_score_bigquery = get_best_score_from_bigquery(project_id, dataset_id, table_id)

    print(f"Best score from BigQuery: {best_score_bigquery}")

    if not best_score_bigquery:
        print("No best score found in BigQuery.")
        return None

    experiment_id = best_score_bigquery["experiment_id"]

    try:
        # Initialize GCS client
        storage_client = storage.Client()

        # Get source bucket and blob
        source_bucket = storage_client.bucket(source_bucket_name)
        source_blob = source_bucket.blob(f"experiment1/{experiment_id}.json")

        # Get destination bucket (can be the same as source)
        destination_bucket = storage_client.bucket(destination_bucket_name)

        # Copy the blob
        source_bucket.copy_blob(source_blob, destination_bucket, destination_blob_name)

        print(
            f"File copied successfully: {source_bucket_name}/{experiment_id}.json → {destination_bucket_name}/{destination_blob_name}"
        )

        # Add copy information to the result
        best_score_bigquery["source_blob"] = f"{source_bucket_name}/{experiment_id}"
        best_score_bigquery["destination_blob"] = (
            f"{destination_bucket_name}/{destination_blob_name}"
        )

        return best_score_bigquery

    except Exception as e:
        print(f"Error copying blob in GCS: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    best_prompt = upgrade_best_prompt(
        project_id="dan-ml-learn-6-ffaf",
        dataset_id="experiment1",
        table_id="experiment_scores",
        source_bucket_name="dan-ml-learn-6-ffaf-experiments",
        destination_bucket_name="dan-ml-learn-6-ffaf-experiments",
        destination_blob_name="experiment1/best_prompt_latest.json",
    )
