import pytest
from unittest.mock import MagicMock, patch
from backend.models import Book, DuplicateFilePathError, InvalidFilePathError

class MockBase:
    def __init__(self):
        pass

@patch('backend.models.Book.check_file_path_exists', return_value=True)
@patch('backend.models.Book.check_file_path_uniqueness', return_value=True)
def test_book_creation(mock_uniqueness, mock_exists):
    book = Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path="/path/to/test.pdf")
    assert book.id == 1
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.category == "Test Category"
    assert book.cover_image_url == "test.jpg"
    assert book.file_path == "/path/to/test.pdf"

@patch('backend.models.Book.check_file_path_exists', return_value=True)
@patch('backend.models.Book.check_file_path_uniqueness', return_value=True)
def test_book_creation_missing_fields(mock_uniqueness, mock_exists):
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert book.id is None
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.category == "Test Category"
    assert book.cover_image_url is None
    assert book.file_path == "/path/to/test.pdf"

@patch('backend.models.Book.check_file_path_exists', return_value=True)
@patch('backend.models.Book.check_file_path_uniqueness', return_value=True)
def test_book_creation_empty_fields(mock_uniqueness, mock_exists):
    book = Book(title="", author="", category="", file_path="")
    assert book.title == ""
    assert book.author == ""
    assert book.category == ""
    assert book.file_path == ""

@patch('backend.models.Book.check_file_path_exists', return_value=False)
@patch('backend.models.Book.check_file_path_uniqueness', return_value=True)
def test_book_creation_invalid_file_path(mock_uniqueness, mock_exists):
    with pytest.raises(InvalidFilePathError) as e:
        Book(title="Test Book", author="Test Author", category="Test Category", file_path="test.pdf")
    assert "file_path" in str(e.value)

@patch('backend.models.Book.check_file_path_exists', return_value=True)
@patch('backend.models.Book.check_file_path_uniqueness', return_value=False)
def test_book_creation_duplicate_file_path(mock_uniqueness, mock_exists):
    with pytest.raises(DuplicateFilePathError) as e:
        Book(title="Test Book 1", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert "unique" in str(e.value)


@patch('backend.models.Book.check_file_path_exists', return_value=True)
@patch('backend.models.Book.check_file_path_uniqueness', return_value=True)
def test_book_representation(mock_uniqueness, mock_exists):
    book = Book(id=1, title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert str(book) == "<Book id=1 title='Test Book' author='Test Author' category='Test Category' file_path='/path/to/test.pdf'>"

def test_book_creation_invalid_category():
    with pytest.raises(ValueError) as e:
        Book(id=1, title="Test Book", author="Test Author", category=123, file_path="/path/to/test.pdf")
    assert "Category must be a string" in str(e.value)

def test_book_creation_invalid_title():
    with pytest.raises(ValueError) as e:
        Book(id=1, title=123, author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert "Title must be a string" in str(e.value)

def test_book_creation_invalid_author():
    with pytest.raises(ValueError) as e:
        Book(id=1, title="Test Book", author=123, category="Test Category", file_path="/path/to/test.pdf")
    assert "Author must be a string" in str(e.value)

def test_book_creation_invalid_file_path_type():
    with pytest.raises(TypeError) as e:
        Book(id=1, title="Test Book", author="Test Author", category="Test Category", file_path=123)
    assert "file_path must be a string" in str(e.value)

def test_book_creation_invalid_cover_image_url_type():
    with pytest.raises(TypeError) as e:
        Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url=123, file_path="/path/to/test.pdf")
    assert "cover_image_url must be a string" in str(e.value)

def test_book_creation_with_none_values():
    book = Book(id=1, title=None, author=None, category=None, cover_image_url=None, file_path=None)
    assert book.title is None
    assert book.author is None
    assert book.category is None
    assert book.cover_image_url is None
    assert book.file_path is None

def test_book_creation_with_special_characters():
    book = Book(id=1, title="Test Book !@#$%^&*()", author="Test Author <>?", category="Test Category []{}", cover_image_url="test.jpg", file_path="/path/to/test.pdf")
    assert book.title == "Test Book !@#$%^&*()"
    assert book.author == "Test Author <>?"
    assert book.category == "Test Category []{}"

def test_book_creation_with_long_title():
    long_title = "a" * 256
    book = Book(id=1, title=long_title, author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path="/path/to/test.pdf")
    assert len(book.title) == 256

def test_book_creation_with_long_author():
    long_author = "a" * 256
    book = Book(id=1, title="Test Book", author=long_author, category="Test Category", cover_image_url="test.jpg", file_path="/path/to/test.pdf")
    assert len(book.author) == 256

def test_book_creation_with_long_category():
    long_category = "a" * 256
    book = Book(id=1, title="Test Book", author="Test Author", category=long_category, cover_image_url="test.jpg", file_path="/path/to/test.pdf")
    assert len(book.category) == 256

def test_book_creation_with_long_file_path():
    long_file_path = "/a/long/path/to/a/file" * 10
    book = Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path=long_file_path)
    assert len(book.file_path) == len(long_file_path)

def test_book_creation_with_long_cover_image_url():
    long_cover_image_url = "a" * 256
    book = Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url=long_cover_image_url, file_path="/path/to/test.pdf")
    assert len(book.cover_image_url) == 256
