build:
	docker build --progress=plain --platform=linux/amd64 -t us-central1-docker.pkg.dev/dan-ml-learn-6-ffaf/ereader-easy-swedish/experiment:latest .
push:
	docker push us-central1-docker.pkg.dev/dan-ml-learn-6-ffaf/ereader-easy-swedish/experiment:latest

buildpush: build push