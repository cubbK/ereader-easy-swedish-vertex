import kfp
from google.cloud import aiplatform

import google.cloud.aiplatform as aip

from kfp import compiler
from kfp.v2.dsl import component

project_id = "dan-ml-learn-6-ffaf"
pipeline_root_path = "gs://dan-ml-learn-6-ffaf-experiments/experiment1_pipeline_root"


@component(
    base_image="us-central1-docker.pkg.dev/dan-ml-learn-6-ffaf/ereader-easy-swedish/experiment:latest"
)
def experiment_component():
    # Import and run your experiment inside the component
    from src.experiments.experiment1 import run_experiment

    run_experiment()


# Define the workflow of the pipeline.
@kfp.dsl.pipeline(name="experiment1_pipeline", pipeline_root=pipeline_root_path)
def pipeline(project_id: str):
    print("Running the experiment1 pipeline...")
    experiment_task = experiment_component()


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=pipeline,  # type: ignore
        package_path="experiment1_pipeline.yaml",
    )

    aip.init(
        project=project_id,
        location="us-central1",
    )
    job = aip.PipelineJob(
        display_name="experiment1_pipeline",
        template_path="experiment1_pipeline.yaml",
        pipeline_root=pipeline_root_path,
        parameter_values={"project_id": project_id},
    )

    job.submit(
        service_account="my-service-account2@dan-ml-learn-6-ffaf.iam.gserviceaccount.com"
    )
