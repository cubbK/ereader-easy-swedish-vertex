import functions_framework
from google.cloud import aiplatform


@functions_framework.cloud_event
def trigger_pipeline(cloud_event):
    pipeline_root_path = (
        "gs://dan-ml-learn-6-ffaf-experiments/experiment1_pipeline_root"
    )

    bucket = cloud_event.data["bucket"]
    name = cloud_event.data["name"]

    print(f"New file uploaded: gs://{bucket}/{name}")

    aiplatform.init(project="dan-ml-learn-6-ffaf", location="us-central1")

    pipeline_job = aiplatform.PipelineJob(
        display_name="experiment1-auto-triggered",
        template_path="gs://dan-ml-learn-6-ffaf-experiments/experiment1_pipeline/experiment1_pipeline.json",
        pipeline_root=pipeline_root_path,
        parameter_values={
            # "book_src": f"gs://{bucket}/{name}",
            "project_id": "dan-ml-learn-6-ffaf",
        },
    )

    pipeline_job.run(
        service_account="my-service-account2@dan-ml-learn-6-ffaf.iam.gserviceaccount.com",
    )
