import os
import re
import pypandoc


class Book:
    def __init__(self, book_path: str):
        """
        Initialize a Book object with the path to an EPUB file.

        Args:
            book_path (str): Path to the EPUB file
        """
        if not os.path.exists(book_path):
            raise FileNotFoundError(f"Book file not found: {book_path}")

        if not book_path.lower().endswith(".epub"):
            raise ValueError(f"File is not an EPUB: {book_path}")

        self.book_path = book_path
        self.raw: str = ""
        self.chunks = []

        self._load_book()
        self._chunk_book()

    def _load_book(self):
        """
        Load the EPUB book and extract its content.
        """
        filter_script = os.path.join(os.path.dirname(__file__), "./remove_images.py")

        output = pypandoc.convert_file(
            self.book_path,
            "plain",
            format="epub",
            extra_args=["--filter", filter_script],
        )

        self.raw = output

    def _chunk_book(self):
        paragraphs = re.split(r"\n\s*\n", self.raw)

        paragraphs = list(
            map(
                lambda p: re.sub(
                    r"\s+", " ", re.sub(r"--+", "", re.sub(r"\n", " ", p))
                ).strip(),  # Remove dash sequences and newlines
                paragraphs,
            )
        )

        chunk_len = 0
        chunk = ""
        for paragraph in paragraphs:
            chunk += paragraph + "\n"
            chunk_len += len(paragraph)
            if chunk_len > 2000:
                self.chunks.append(chunk)
                chunk = ""
                chunk_len = 0

    def get_random_chunks(self, number_of: int):
        """
        Get a random sample of chunks from the book.

        Args:
            number_of (int): Number of random chunks to return.

        Returns:
            list: List of random chunks.
        """
        import random

        return random.sample(self.chunks, number_of)
