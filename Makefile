build:
	docker build --progress=plain --platform=linux/amd64 -t us-central1-docker.pkg.dev/dan-ml-learn-6-ffaf/ereader-easy-swedish/experiment:latest .
push:
	docker push us-central1-docker.pkg.dev/dan-ml-learn-6-ffaf/ereader-easy-swedish/experiment:latest

buildpush: build push

trigger_pipeline:
	python -m src.experiments.experiment1_pipeline

prepare_function:
	uv pip compile --output-file=./src/functions/trigger_experiment1_pipeline/requirements.txt ./pyproject.toml

deploy_function: 
	gcloud functions deploy trigger_experiment1_pipeline --gen2 --runtime=python310 --region=us-central1 --memory=512MB --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=dan-ml-learn-6-ffaf-books" --entry-point=trigger_pipeline --source=./src/functions/trigger_experiment1_pipeline --set-env-vars=GOOGLE_PROJECT=dan-ml-learn-6-ffaf --service-account=my-service-account2@dan-ml-learn-6-ffaf.iam.gserviceaccount.com

terraform_apply:
	cd terraform && terraform init && terraform apply -auto-approve


deploy_all: terraform_apply buildpush prepare_function deploy_function