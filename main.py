from src.experiment import Experiment
from src.book import Book
from src.llm import prompt_template_1

if __name__ == "__main__":
    book1 = Book("./data/books/book1.epub")

    chunks = book1.get_random_chunks(2)

    experiments = [
        Experiment(
            chunk=chunk["chunk"],
            previous_chunk=chunk["previous_chunk"],
            after_chunk=chunk["after_chunk"],
        )
        for chunk in chunks
    ]

    for experiment in experiments:
        result, score = experiment.run(prompt_template_1)
        print(f"Result: {result}")
        print(f"Score: {score}")
