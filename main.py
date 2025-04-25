from src.book import Book

if __name__ == "__main__":
    book1 = Book("./data/books/book1.epub")

    chunks = book1.get_random_chunks(2)
