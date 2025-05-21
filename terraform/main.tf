provider "google" {
  project = "dan-ml-learn-6-ffaf"
  region  = "us-central1"
}

resource "google_storage_bucket" "data_bucket" {
  name     = "dan-ml-learn-6-ffaf-experiments"
  location = "us-central1"

  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "experiment1" {
  dataset_id = "experiment1"
  location   = "us-central1"
}

resource "google_service_account" "my_sa" {
  account_id   = "my-service-account2"
  display_name = "My Service Account2"
}

# 2. Assign IAM roles to the service account at the project level
resource "google_project_iam_member" "sa_roles" {
  for_each = toset([
    "roles/aiplatform.serviceAgent",
    "roles/aiplatform.user",
    "roles/editor",
    "roles/firebasevertexai.admin",
    "roles/storage.objectUser",
    "roles/storage.objectViewer",
    "roles/aiplatform.admin",
    "roles/secretmanager.secretAccessor"
  ])

  project = "dan-ml-learn-6-ffaf"
  role    = each.value
  member  = "serviceAccount:${google_service_account.my_sa.email}"
}
