# Evolve Prompt Pipeline

A machine learning pipeline built on Google Cloud Vertex AI used to train and find the best prompt for translating books.
I wanted to do the enterprise way like teams in real projects do.

Using https://dspy.ai/ as the evolution framework

![diagram](./diagram.drawio.svg)

## Getting started

Install deps locally. Using https://github.com/astral-sh/uv :

```bash
uv sync
```

Deploy everything to cloud. This is applying terraform, deploying the function and pushing the docker image:

```bash
gcloud auth login
gcloud auth application-default login
make deploy_all
```

Trigger pipeline from local:

```bash
gcloud auth application-default login
make trigger_pipeline
```
