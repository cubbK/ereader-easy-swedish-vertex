import datetime

from google.cloud import aiplatform


if __name__ == "__main__":
    aiplatform.init(
        experiment="experiment1", project="dan-ml-learn-6-ffaf", location="us-central1"
    )

    run_name = f"run-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    aiplatform.start_run(run=run_name)

    params = {
        "param1": "value1",
        "param2": "value2",
        "param3": "value3",
    }

    aiplatform.log_params(params)

    aiplatform.log_time_series_metrics({"accuracy": 0.85})
    aiplatform.log_time_series_metrics({"accuracy": 0.90})

    aiplatform.end_run()
