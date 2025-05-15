from google.cloud import storage
import os


def upload_to_gcs(local_file_path, gcs_uri):
    """
    Upload a local file to Google Cloud Storage.

    Args:
        local_file_path (str): Path to the local file (e.g., 'outputs/best_prompt.json')
        gcs_uri (str): Target GCS URI (e.g., 'gs://my-bucket/experiments/exp123/run456/best_prompt.json')
    """
    if not gcs_uri.startswith("gs://"):
        raise ValueError("gcs_uri must start with 'gs://'")

    # Extract bucket and blob name
    parts = gcs_uri[5:].split("/", 1)
    bucket_name = parts[0]
    blob_path = parts[1]

    # Create a GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    # Upload the file
    blob.upload_from_filename(local_file_path)

    print(f"✅ Uploaded '{local_file_path}' to '{gcs_uri}'")


# Example usage
# upload_to_gcs(
#     local_file_path="outputs/best_prompt.json",
#     gcs_uri="gs://my-bucket/experiments/exp123/run456/best_prompt.json",
# )
