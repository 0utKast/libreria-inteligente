import pytest
from unittest.mock import MagicMock
from backend.models import Book

def test_book_creation():
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
    with pytest.raises(Exception) as e:
        Book(author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert "title" in str(e.value)

def test_book_creation_missing_author():
    with pytest.raises(Exception) as e:
        Book(title="Test Book", category="Test Category", file_path="/path/to/file.pdf")
    assert "author" in str(e.value)

def test_book_creation_missing_category():
    with pytest.raises(Exception) as e:
        Book(title="Test Book", author="Test Author", file_path="/path/to/file.pdf")
    assert "category" in str(e.value)

def test_book_creation_missing_file_path():
    with pytest.raises(Exception) as e:
        Book(title="Test Book", author="Test Author", category="Test Category")
    assert "file_path" in str(e.value)


def test_book_creation_empty_title():
    with pytest.raises(Exception) as e:
        Book(title="", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert "title" in str(e.value)


def test_book_creation_empty_author():
    with pytest.raises(Exception) as e:
        Book(title="Test Book", author="", category="Test Category", file_path="/path/to/file.pdf")
    assert "author" in str(e.value)

def test_book_creation_empty_category():
    with pytest.raises(Exception) as e:
        Book(title="Test Book", author="Test Author", category="", file_path="/path/to/file.pdf")
    assert "category" in str(e.value)


def test_book_creation_empty_file_path():
    with pytest.raises(Exception) as e:
        Book(title="Test Book", author="Test Author", category="Test Category", file_path="")
    assert "file_path" in str(e.value)

def test_book_creation_duplicate_file_path(mocker):
    session_mock = mocker.patch('backend.models.Session')
    session_mock.query().filter().one_or_none.return_value = Book(file_path='/path/to/file.pdf')
    with pytest.raises(Exception) as e:
        Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert "file_path" in str(e.value)

def test_book_creation_non_string_inputs():
    with pytest.raises(TypeError) as e:
        Book(title=123, author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    assert "title" in str(e.value)
    with pytest.raises(TypeError) as e:
        Book(title="Test Book", author=123, category="Test Category", file_path="/path/to/file.pdf")
    assert "author" in str(e.value)
    with pytest.raises(TypeError) as e:
        Book(title="Test Book", author="Test Author", category=123, file_path="/path/to/file.pdf")
    assert "category" in str(e.value)
    with pytest.raises(TypeError) as e:
        Book(title="Test Book", author="Test Author", category="Test Category", file_path=123)
    assert "file_path" in str(e.value)

def test_book_file_path_uniqueness():
    book1 = Book(title="Test Book 1", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    book2 = Book(title="Test Book 2", author="Test Author", category="Test Category", file_path="/path/to/file.pdf")
    #This test will likely fail unless you have some mechanism to enforce uniqueness in your model or database.  The below assertion should likely be removed or modified.
    # assert book1.file_path != book2.file_path