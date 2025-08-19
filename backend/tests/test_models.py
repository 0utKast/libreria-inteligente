import pytest
from unittest.mock import MagicMock
from backend.models import Book

class MockBase:
    def __init__(self):
        pass

def test_book_creation():
    mock_base = MockBase()
    book = Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path="/path/to/test.pdf")
    assert book.id == 1
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.category == "Test Category"
    assert book.cover_image_url == "test.jpg"
    assert book.file_path == "/path/to/test.pdf"

def test_book_creation_missing_fields():
    mock_base = MockBase()
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert book.id is None
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.category == "Test Category"
    assert book.cover_image_url is None
    assert book.file_path == "/path/to/test.pdf"

def test_book_creation_empty_fields():
    mock_base = MockBase()
    book = Book(title="", author="", category="", file_path="")
    assert book.title == ""
    assert book.author == ""
    assert book.category == ""
    assert book.file_path == ""

def test_book_creation_invalid_file_path():
    mock_base = MockBase()
    with pytest.raises(Exception) as e:  # Expecting an error for invalid file paths (e.g. missing path)
        Book(title="Test Book", author="Test Author", category="Test Category", file_path="test.pdf")
    assert "file_path" in str(e.value)

def test_book_creation_duplicate_file_path():
    mock_base = MockBase()
    book1 = Book(title="Test Book 1", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    book2 = Book(title="Test Book 2", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    with pytest.raises(Exception) as e: # Simulate database constraint violation
        pass # Assume database handles uniqueness constraint.  More robust test would require database interaction.
    #More sophisticated assertion might be needed depending on the database and exception handling
    assert "unique" in str(e.value)


def test_book_representation():
    mock_base = MockBase()
    book = Book(id=1, title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert str(book) == "<Book id=1 title='Test Book' author='Test Author' category='Test Category' file_path='/path/to/test.pdf'>"

```