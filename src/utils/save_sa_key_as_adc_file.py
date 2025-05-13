import os
from google.cloud import secretmanager


def save_sa_key_as_adc_file(secret_id="vertex-sa-key", project_id="your-project-id"):
    # Create Secret Manager client using default credentials
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})
    sa_key = response.payload.data.decode("UTF-8")

    # Save it to the expected ADC location
    credentials_path = "/root/.config/gcloud/application_default_credentials.json"
    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
    with open(credentials_path, "w") as f:
        f.write(sa_key)

    # Set the ADC environment variable (if needed explicitly)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
