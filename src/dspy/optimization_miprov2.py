from typing import Literal
import dspy
from src.dspy.metric import TranslationMetric
from src.dspy.translator import translator
from src.dspy.evaluator import trainset as trainset_input


def optimize_translator(trainset, metric, auto: Literal["light", "medium", "heavy"]):
    """
    Optimize the translator using MIPROv2 with zero-shot configuration.
    """

    teleprompter = dspy.MIPROv2(metric=metric, auto=auto)

    print("Optimizing zero-shot program with MIPRO...")
    zeroshot_optimized_program = teleprompter.compile(
        translator.deepcopy(),
        trainset=trainset,
        max_bootstrapped_demos=0,  # ZERO FEW-SHOT EXAMPLES
        max_labeled_demos=0,  # ZERO FEW-SHOT EXAMPLES
        requires_permission_to_run=False,
    )

    return zeroshot_optimized_program


if __name__ == "__main__":
    metric = TranslationMetric()

    optimized = optimize_translator(
        trainset=trainset_input, auto="light", metric=metric
    )
    optimized.save("translator_optimized.json")

    test_example = "Folly, folly, his heart kept saying: conscious, gratuitous, suicidal folly. Of all the crimes that a Party member could commit, this one was the least possible to conceal. Actually the idea had first floated into his head in the form of a vision, of the glass paperweight mirrored by the surface of the gateleg table. As he had foreseen, Mr Charrington had made no difficulty about letting the room. He was obviously glad of the few dollars that it would bring him. Nor did he seem shocked or become offensively knowing when it was made clear that Winston wanted the room for the purpose of a love-affair. Instead he looked into the middle distance and spoke in generalities, with so delicate an air as to give the impression that he had become partly invisible. Privacy, he said, was a very valuable thing. Everyone wanted a place where they could be alone occasionally. And when they had such a place, it was only common courtesy in anyone else who knew of it to keep his knowledge to himself. He even, seeming almost to fade out of existence as he did so, added that there were two entries to the house, one of them through the back yard, which gave on an alley."

    original_result = translator(test_example)
    optimized_result = optimized(test_example)

    print("Original Translator:")
    print(f"Easy English: {original_result['easy_english']}")
    print(f"Swedish: {original_result['swedish']}")
    print("\nOptimized Translator:")
    print(f"Easy English: {optimized_result['easy_english']}")
    print(f"Swedish: {optimized_result['swedish']}")

    metric = TranslationMetric()
    original_score = metric(dspy.Example(english=test_example), original_result)
    optimized_score = metric(dspy.Example(english=test_example), optimized_result)

    print(f"\nOriginal Score: {original_score:.4f}")
    print(f"Optimized Score: {optimized_score:.4f}")
