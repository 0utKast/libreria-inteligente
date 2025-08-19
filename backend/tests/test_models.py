import pytest
from unittest.mock import MagicMock
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
    with pytest.raises(Exception) as e:  # Expecting an error because title can't be empty in database
        Book(title="", author="Author", category="Category", file_path="/path/to/file.pdf")
    assert "title" in str(e.value)


def test_book_creation_empty_author():
    with pytest.raises(Exception) as e: # Expecting an error because author can't be empty in database
        Book(title="Title", author="", category="Category", file_path="/path/to/file.pdf")
    assert "author" in str(e.value)


def test_book_creation_empty_category():
    with pytest.raises(Exception) as e: # Expecting an error because category can't be empty in database
        Book(title="Title", author="Author", category="", file_path="/path/to/file.pdf")
    assert "category" in str(e.value)

def test_book_creation_duplicate_file_path():
    book1 = Book(title="Book1", author="Author1", category="Category1", file_path="/path/to/file.pdf")
    with pytest.raises(Exception) as e: #Simulate database constraint error for duplicate file_path
        book2 = Book(title="Book2", author="Author2", category="Category2", file_path="/path/to/file.pdf")
    assert "unique constraint" in str(e.value) #this assertion might need adaptation depending on your database and error message


def test_book_creation_invalid_file_path():
    with pytest.raises(Exception) as e: # Simulate an error for an invalid file path (e.g., too long)
        Book(title="Title", author="Author", category="Category", file_path="a"*1000) # very long path
    assert "file_path" in str(e.value) #Adapt as needed, it's a generic error check



```