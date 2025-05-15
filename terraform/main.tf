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