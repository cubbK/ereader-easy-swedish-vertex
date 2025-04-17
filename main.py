from src.book import Book
from src.run_experiment import get_readability_score, run_experiment
import vertexai

# vertexai.init(
#     project="dan-ml-learn-5-b42c",
#     location="us-central1",
#     api_endpoint="aiplatform.googleapis.com",
# )

if __name__ == "__main__":
    book1 = Book("./data/books/book1.epub")

    print(book1.chunks)  # type: ignore
