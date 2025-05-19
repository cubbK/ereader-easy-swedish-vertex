from google.cloud import aiplatform


# Initialize Vertex AI with staging bucket
aiplatform.init(
    project="dan-ml-learn-6-ffaf",
    location="us-central1",
    staging_bucket="gs://dan-ml-learn-6-ffaf-staging",
)

# Define container image path in Artifact Registry
IMAGE_URI = "us-central1-docker.pkg.dev/dan-ml-learn-6-ffaf/ereader-easy-swedish/experiment:latest"

# Create and submit custom job
job = aiplatform.CustomJob(
    display_name="experiment1-custom-job",
    worker_pool_specs=[
        {
            "machine_spec": {
                "machine_type": "n1-standard-4",
                "accelerator_type": "NVIDIA_TESLA_T4",
                "accelerator_count": 1,
            },
            "replica_count": 1,
            "container_spec": {
                "image_uri": IMAGE_URI,
                # No need for explicit command/args if your ENTRYPOINT is correct
            },
        },
    ],
)

job.run(
    service_account="my-service-account2@dan-ml-learn-6-ffaf.iam.gserviceaccount.com",
    enable_web_access=True,
)

print(f"Job launched. View job details at: {job.display_name}")
