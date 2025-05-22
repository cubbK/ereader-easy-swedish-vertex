provider "google" {
  project = "dan-ml-learn-6-ffaf"
  region  = "us-central1"
}

resource "google_storage_bucket" "data_bucket" {
  name     = "dan-ml-learn-6-ffaf-experiments"
  location = "us-central1"

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "data_bucket_2" {
  name     = "dan-ml-learn-6-ffaf-books"
  location = "us-central1"

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "default_book" {
  name   = "experiment1_pipeline/experiment1_pipeline.json"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../experiment1_pipeline.json"
}

resource "google_storage_bucket_object" "pipeline_yaml" {
  name   = "book1.epub"
  bucket = google_storage_bucket.data_bucket_2.name
  source = "${path.module}/../data/books/book1.epub"
}

resource "google_bigquery_dataset" "experiment1" {
  dataset_id = "experiment1"
  location   = "us-central1"
}

resource "google_service_account" "my_sa" {
  account_id   = "my-service-account2"
  display_name = "My Service Account2"
}

resource "google_project_iam_member" "sa_roles" {
  for_each = toset([
    "roles/aiplatform.serviceAgent",
    "roles/aiplatform.user",
    "roles/editor",
    "roles/firebasevertexai.admin",
    "roles/storage.objectUser",
    "roles/storage.objectViewer",
    "roles/aiplatform.admin",
    "roles/secretmanager.secretAccessor",
    "roles/cloudbuild.builds.builder",
    "roles/eventarc.eventReceiver",
    "roles/pubsub.publisher"
  ])

  project = "dan-ml-learn-6-ffaf"
  role    = each.value
  member  = "serviceAccount:${google_service_account.my_sa.email}"
}

data "google_project" "project" {
  project_id = "dan-ml-learn-6-ffaf"
}


resource "google_project_iam_member" "gcs_publish" {
  project = "dan-ml-learn-6-ffaf"
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:service-${data.google_project.project.number}@gs-project-accounts.iam.gserviceaccount.com"
}

