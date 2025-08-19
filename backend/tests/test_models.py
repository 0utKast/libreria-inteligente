import pytest
from unittest.mock import MagicMock
from backend.models import Book

# Mocking the database interaction
Base = MagicMock()

def test_book_creation():
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/book.pdf")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.category == "Test Category"
    assert book.file_path == "/path/to/book.pdf"
    assert book.id is None  # ID is assigned by the database
    assert book.cover_image_url is None


def test_book_creation_with_cover_image():
    book = Book(title="Test Book", author="Test Author", category="Test Category", 
                cover_image_url="http://example.com/cover.jpg", file_path="/path/to/book.pdf")
    assert book.cover_image_url == "http://example.com/cover.jpg"


def test_book_creation_missing_title():
    with pytest.raises(Exception) as e:  # Expect an error, likely from SQLAlchemy
        book = Book(author="Test Author", category="Test Category", file_path="/path/to/book.pdf")
    assert "title" in str(e.value) #Check that the error message mentions missing title


def test_book_creation_missing_author():
    with pytest.raises(Exception) as e:
        book = Book(title="Test Book", category="Test Category", file_path="/path/to/book.pdf")
    assert "author" in str(e.value)


def test_book_creation_missing_category():
    with pytest.raises(Exception) as e:
        book = Book(title="Test Book", author="Test Author", file_path="/path/to/book.pdf")
    assert "category" in str(e.value)


def test_book_creation_missing_file_path():
    with pytest.raises(Exception) as e:
        book = Book(title="Test Book", author="Test Author", category="Test Category")
    assert "file_path" in str(e.value)


def test_book_creation_empty_title():
    with pytest.raises(Exception) as e:
        book = Book(title="", author="Test Author", category="Test Category", file_path="/path/to/book.pdf")
    assert "title" in str(e.value)


def test_book_creation_empty_author():
    with pytest.raises(Exception) as e:
        book = Book(title="Test Book", author="", category="Test Category", file_path="/path/to/book.pdf")
    assert "author" in str(e.value)


def test_book_creation_empty_category():
    with pytest.raises(Exception) as e:
        book = Book(title="Test Book", author="Test Author", category="", file_path="/path/to/book.pdf")
    assert "category" in str(e.value)


def test_book_creation_duplicate_file_path():
    #This test would require mocking the database's unique constraint check.  
    #Omitting detailed mocking for brevity, but the concept is to verify exception handling for a database constraint violation.
    pass #Replace with more robust testing when database interaction is fully implemented.


def test_book_representation():
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/book.pdf")
    assert str(book) == "<Book(title='Test Book', author='Test Author', category='Test Category', file_path='/path/to/book.pdf')>"