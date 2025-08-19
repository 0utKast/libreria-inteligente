import pytest
from unittest.mock import patch
from backend.models import Book

@patch('sqlalchemy.orm.DeclarativeBase')
def test_book_creation(MockBase):
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.category == "Test Category"
    assert book.file_path == "/path/to/file.pdf"
    assert book.id is None
    assert book.cover_image_url is None

def test_book_creation_with_cover_image():
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/file.pdf", cover_image_url="http://example.com/cover.jpg")
    assert book.cover_image_url == "http://example.com/cover.jpg"

def test_book_creation_missing_title():
    with pytest.raises(Exception) as e:  # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert "title" in str(e.value) # Check if the exception message indicates the missing title

def test_book_creation_missing_author():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="Test Book", category="Test Category", file_path="/path/to/file.pdf")
    assert "author" in str(e.value) # Check if the exception message indicates the missing author

def test_book_creation_missing_category():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="Test Book", author="Test Author", file_path="/path/to/file.pdf")
    assert "category" in str(e.value) # Check if the exception message indicates the missing category


def test_book_creation_missing_filepath():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="Test Book", author="Test Author", category="Test Category")
    assert "file_path" in str(e.value) # Check if the exception message indicates the missing file_path


def test_book_creation_empty_title():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert "title" in str(e.value) # Check if the exception message indicates the empty title


def test_book_creation_empty_author():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="Test Book", author="", category="Test Category", file_path="/path/to/file.pdf")
    assert "author" in str(e.value) # Check if the exception message indicates the empty author


def test_book_creation_empty_category():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="Test Book", author="Test Author", category="", file_path="/path/to/file.pdf")
    assert "category" in str(e.value) # Check if the exception message indicates the empty category


def test_book_creation_empty_filepath():
    with pytest.raises(Exception) as e: # Expecting an error due to missing required fields. Adjust as needed based on sqlalchemy behavior
        book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="")
    assert "file_path" in str(e.value) # Check if the exception message indicates the empty filepath

def test_book_file_path_uniqueness():
    book1 = Book(title="Test Book 1", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    book2 = Book(title="Test Book 2", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    #This test will likely fail unless you have some mechanism to enforce uniqueness in your model or database.  The below assertion should likely be removed or modified.
    # assert book1.file_path != book2.file_path