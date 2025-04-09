from src.run_experiment import run_experiment
import vertexai

vertexai.init(
    project="dan-ml-learn-5-b42c",
    location="us-central1",
    api_endpoint="aiplatform.googleapis.com",
)

if __name__ == "__main__":
    with open("text/train.txt", "r") as file:
        train_text = file.read()

    with open("text/train_after.txt", "r") as file:
        train_text_after = file.read()

    run_experiment(["v1"], train_text, train_text_after, "")
    run_experiment(["v2_1", "v2_2"], train_text, train_text_after, "")
