from src.book import Book
from src.llm_direct import LLM

if __name__ == "__main__":
    book1 = Book("./data/books/book1.epub")

    chunks = book1.get_random_chunks(2)

    llm = LLM()
    response = llm.prompt("Hello, how are you today?")
    print(response)
