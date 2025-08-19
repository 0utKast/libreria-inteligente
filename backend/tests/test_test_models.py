import pytest
from unittest.mock import MagicMock, patch
from backend.models import Book

# Mock de la clase Base de SQLAlchemy
class MockBase:
    metadata = MagicMock()

# Reemplazar la clase Base real con el mock
Book.metadata = MockBase.metadata

def test_book_creation():
    book = Book(title="Clean Code", author="Robert Martin", category="Software Engineering", cover_image_url="url", file_path="/path/to/file.pdf")
    assert book.title == "Clean Code"
    assert book.author == "Robert Martin"
    assert book.category == "Software Engineering"
    assert book.cover_image_url == "url"
    assert book.file_path == "/path/to/file.pdf"

def test_book_creation_no_cover_image():
    book = Book(title="Test Driven Development", author="Kent Beck", category="Software Engineering", file_path="/path/to/file.pdf")
    assert book.cover_image_url is None

def test_book_creation_empty_title():
    with pytest.raises(ValueError) as e:
        Book(title="", author="Author", category="Category", file_path="/path/to/file.pdf")
    assert "title cannot be empty" in str(e.value)

def test_book_creation_empty_author():
    with pytest.raises(ValueError) as e:
        Book(title="Title", author="", category="Category", file_path="/path/to/file.pdf")
    assert "author cannot be empty" in str(e.value)

def test_book_creation_empty_category():
    with pytest.raises(ValueError) as e:
        Book(title="Title", author="Author", category="", file_path="/path/to/file.pdf")
    assert "category cannot be empty" in str(e.value)

@patch('backend.models.Book.check_file_path_uniqueness', side_effect=Exception("Unique constraint failed"))
def test_book_creation_duplicate_file_path(mock_check):
    book1 = Book(title="Book1", author="Author1", category="Category1", file_path="/path/to/file.pdf")
    with pytest.raises(Exception) as e:
        book2 = Book(title="Book2", author="Author2", category="Category2", file_path="/path/to/file.pdf")
    assert "Unique constraint failed" in str(e.value)

@patch('backend.models.Book.validate_file_path')
def test_book_creation_invalid_file_path(mock_validate):
    mock_validate.side_effect = ValueError("Invalid file path")
    with pytest.raises(ValueError) as e:
        Book(title="Title", author="Author", category="Category", file_path="a"*1000)
    assert "Invalid file path" in str(e.value)

def test_book_creation_long_title():
    long_title = "a" * 256  # Simulate a title exceeding the database limit
    with pytest.raises(ValueError) as e:
        Book(title=long_title, author="Author", category="Category", file_path="/path/to/file.pdf")
    assert "title exceeds maximum length" in str(e.value)

def test_book_creation_long_author():
    long_author = "a" * 256  # Simulate an author name exceeding the database limit
    with pytest.raises(ValueError) as e:
        Book(title="Title", author=long_author, category="Category", file_path="/path/to/file.pdf")
    assert "author exceeds maximum length" in str(e.value)

def test_book_creation_long_category():
    long_category = "a" * 256  # Simulate a category name exceeding the database limit
    with pytest.raises(ValueError) as e:
        Book(title="Title", author="Author", category=long_category, file_path="/path/to/file.pdf")
    assert "category exceeds maximum length" in str(e.value)

def test_book_creation_long_file_path():
    long_file_path = "a" * 512 # Simulate a file path exceeding the database limit
    with pytest.raises(ValueError) as e:
        Book(title="Title", author="Author", category="Category", file_path=long_file_path)
    assert "file_path exceeds maximum length" in str(e.value)

def test_book_creation_special_characters():
    book = Book(title="Títlê with special characters", author="Authôr", category="Categöry", file_path="/path/to/file.pdf")
    assert book.title == "Títlê with special characters"
    assert book.author == "Authôr"
    assert book.category == "Categöry"


```