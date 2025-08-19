import pytest
from unittest.mock import patch
from backend.models import Book

@patch('backend.models.Base')
def test_book_creation(MockBase):
    book = Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", category="Science Fiction", cover_image_url="url", file_path="/path/to/file.pdf")
    assert book.title == "The Hitchhiker's Guide to the Galaxy"
    assert book.author == "Douglas Adams"
    assert book.category == "Science Fiction"
    assert book.cover_image_url == "url"
    assert book.file_path == "/path/to/file.pdf"

@patch('backend.models.Base')
def test_book_creation_missing_fields(MockBase):
    book = Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", category="Science Fiction")
    assert book.title == "The Hitchhiker's Guide to the Galaxy"
    assert book.author == "Douglas Adams"
    assert book.category == "Science Fiction"
    assert book.cover_image_url is None
    assert book.file_path is None

@patch('backend.models.Base')
def test_book_creation_empty_fields(MockBase):
    book = Book(title="", author="", category="", cover_image_url="", file_path="")
    assert book.title == ""
    assert book.author == ""
    assert book.category == ""
    assert book.cover_image_url == ""
    assert book.file_path == ""

@patch('backend.models.Base')
def test_book_creation_invalid_file_path(MockBase):
    with pytest.raises(Exception) as e:  # Expecting an exception due to unique constraint violation (simulated)
        book1 = Book(title="Book1", author="Author1", category="Category1", file_path="/path/to/file.pdf")
        book2 = Book(title="Book2", author="Author2", category="Category2", file_path="/path/to/file.pdf")

@patch('backend.models.Base')
def test_book_creation_null_values(MockBase):
    book = Book(title=None, author=None, category=None, cover_image_url=None, file_path=None)
    assert book.title is None
    assert book.author is None
    assert book.category is None
    assert book.cover_image_url is None
    assert book.file_path is None

@patch('backend.models.Base')
def test_book_repr(MockBase):
    book = Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", category="Science Fiction", file_path="/path/to/file.pdf")
    expected_repr = "<Book(title='The Hitchhiker\'s Guide to the Galaxy', author='Douglas Adams', category='Science Fiction', file_path='/path/to/file.pdf')>"
    assert repr(book) == expected_repr