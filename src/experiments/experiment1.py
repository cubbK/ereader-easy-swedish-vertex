import datetime

import dspy
from google.cloud import aiplatform

from src.dspy.metric import TranslationMetric
from src.dspy.optimization_miprov2 import optimize_translator
from src.dspy.evaluator import trainset
from src.utils.secret import save_sa_key_to_file

save_sa_key_to_file()

if __name__ == "__main__":
    aiplatform.init(
        experiment="experiment1", project="dan-ml-learn-6-ffaf", location="us-central1"
    )

    run_name = f"run-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    aiplatform.start_run(run=run_name)

    params = {"trainset": trainset, "auto": "light", "metric": TranslationMetric()}

    params_log = {
        "trainset": "trainset_object",
        "auto": params["auto"],
        "metric": params["metric"].__class__.__name__,
    }

    aiplatform.log_params(params_log)

    optimized = optimize_translator(
        trainset=params["trainset"], auto=params["auto"], metric=params["metric"]
    )

    test_example = "Folly, folly, his heart kept saying: conscious, gratuitous, suicidal folly. Of all the crimes that a Party member could commit, this one was the least possible to conceal. Actually the idea had first floated into his head in the form of a vision, of the glass paperweight mirrored by the surface of the gateleg table. As he had foreseen, Mr Charrington had made no difficulty about letting the room. He was obviously glad of the few dollars that it would bring him. Nor did he seem shocked or become offensively knowing when it was made clear that Winston wanted the room for the purpose of a love-affair. Instead he looked into the middle distance and spoke in generalities, with so delicate an air as to give the impression that he had become partly invisible. Privacy, he said, was a very valuable thing. Everyone wanted a place where they could be alone occasionally. And when they had such a place, it was only common courtesy in anyone else who knew of it to keep his knowledge to himself. He even, seeming almost to fade out of existence as he did so, added that there were two entries to the house, one of them through the back yard, which gave on an alley."

    optimized_result = optimized(test_example)

    score = params["metric"](dspy.Example(english=test_example), optimized_result)

    aiplatform.log_time_series_metrics({"score": score})

    aiplatform.end_run()
