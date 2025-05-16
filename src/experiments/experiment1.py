import datetime

import dspy
from google.cloud import aiplatform

from src.dspy.metric import TranslationMetric
from src.dspy.optimization_miprov2 import optimize_translator
from src.dspy.evaluator import trainset, evaluator_dataset
from src.utils.secret import save_sa_key_to_file
from src.utils.storage import upload_to_gcs
from src.utils.log_to_bigquery import log_to_bigquery
from src.utils.upgrade_best_prompt import upgrade_best_prompt
from src.utils.book import Book

save_sa_key_to_file()

if __name__ == "__main__":
    aiplatform.init(
        experiment="experiment1", project="dan-ml-learn-6-ffaf", location="us-central1"
    )

    run_name = f"run-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    aiplatform.start_run(run=run_name)

    book1 = Book("./data/books/book1.epub")
    book1_chunks = book1.get_random_chunks(15)
    book1_examples = [dspy.Example(english=chunk["chunk"]) for chunk in book1_chunks]

    book1_chunks_score = book1.get_random_chunks(15)
    book1_examples_score = [
        dspy.Example(english=chunk["chunk"]) for chunk in book1_chunks_score
    ]

    trainset_all = [*trainset, *book1_examples]

    params = {"trainset": trainset_all, "auto": "light", "metric": TranslationMetric()}

    params_log = {
        "trainset": "trainset_object",
        "auto": params["auto"],
        "metric": params["metric"].__class__.__name__,
    }

    aiplatform.log_params(params_log)

    optimized = optimize_translator(
        trainset=params["trainset"], auto=params["auto"], metric=params["metric"]
    )

    optimized.save("translator_optimized.json")

    upload_to_gcs(
        local_file_path="translator_optimized.json",
        gcs_uri=f"gs://dan-ml-learn-6-ffaf-experiments/experiment1/{run_name}.json",
    )

    evaluator_total_dataset = [*evaluator_dataset, *book1_examples_score]
    score_total = 0
    for example in evaluator_total_dataset:
        print(f"Evaluating example: {example}")

        optimized_result = optimized(example)

        score = params["metric"](dspy.Example(english=example), optimized_result)

        aiplatform.log_time_series_metrics({"score": score})
        score_total += score

    score_total /= len(evaluator_total_dataset)
    log_to_bigquery(
        row={
            "experiment_id": run_name,
            "score": score_total,
            "inserted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
        table_id="dan-ml-learn-6-ffaf.experiment1.experiment_scores",
    )

    upgrade_best_prompt(
        project_id="dan-ml-learn-6-ffaf",
        dataset_id="experiment1",
        table_id="experiment_scores",
        source_bucket_name="dan-ml-learn-6-ffaf-experiments",
        destination_bucket_name="dan-ml-learn-6-ffaf-experiments",
        destination_blob_name="experiment1/best_prompt_latest.json",
    )

    aiplatform.end_run()
