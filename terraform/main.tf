provider "google" {
  project = "dan-ml-learn-5-b42c"
  region  = "us-central1"
}

resource "google_bigquery_dataset" "translation_logs" {
  dataset_id = "translation_logs"
  location   = "US"
}

resource "google_bigquery_table" "experiments" {
  dataset_id = google_bigquery_dataset.translation_logs.dataset_id
  table_id   = "experiments"

  schema = jsonencode([
    { name = "timestamp",      type = "TIMESTAMP", mode = "NULLABLE" },
    { name = "prompt_version", type = "STRING",    mode = "NULLABLE" },
    { name = "input_text",     type = "STRING",    mode = "NULLABLE" },
    { name = "output_text",    type = "STRING",    mode = "NULLABLE" },
    { name = "model_used",     type = "STRING",    mode = "NULLABLE" }
  ])
}
