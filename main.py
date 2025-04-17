from src.book import Book

if __name__ == "__main__":
    book1 = Book("./data/books/book1.epub")

    print(book1.chunks)  # type: ignore
