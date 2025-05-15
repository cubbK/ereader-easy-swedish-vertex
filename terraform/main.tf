provider "google" {
  project = "dan-ml-learn-6-ffaf"
  region  = "us-central1"
}

resource "google_storage_bucket" "data_bucket" {
  name     = "dan-ml-learn-6-ffaf-experiments"
  location = "us-central1"
  
  # Optional but recommended settings
  uniform_bucket_level_access = true
}