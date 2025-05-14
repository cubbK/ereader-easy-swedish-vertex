from google.cloud import secretmanager
import os


def fetch_sa_key(secret_id="my-sa-key"):
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/384047454520/secrets/vertex-sa-key/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def save_sa_key_to_file():
    """Fetches the service account key from Google Secret Manager and saves it to a file. Needed because dspy does not pick up the available google cloud metadata server credentials."""

    key_json = fetch_sa_key(secret_id="vertex-sa-key")
    key_path = "/tmp/service_account.json"
    with open(key_path, "w") as f:
        f.write(key_json)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


if __name__ == "__main__":
    key_json = fetch_sa_key(secret_id="vertex-sa-key")
    print(key_json)
