import pytest
from unittest.mock import Mock, patch
from backend.models import Book

def test_book_creation():
    book = Book(title="The Lord of the Rings", author="J.R.R. Tolkien", category="Fantasy", cover_image_url="url", file_path="/path/to/file.pdf")
    assert book.title == "The Lord of the Rings"
    assert book.author == "J.R.R. Tolkien"
    assert book.category == "Fantasy"
    assert book.cover_image_url == "url"
    assert book.file_path == "/path/to/file.pdf"
    assert book.id is None


def test_book_creation_no_cover_image():
    book = Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", category="Science Fiction", file_path="/path/to/file.txt")
    assert book.cover_image_url is None


def test_book_creation_empty_fields():
    with pytest.raises(ValueError) as e:
        book = Book(title="", author="", category="", cover_image_url="", file_path="")
    assert "file_path cannot be empty" in str(e.value)


@patch('backend.models.Book.save', autospec=True)
def test_book_creation_invalid_file_path_duplicate(mock_save):
    mock_session = Mock()
    mock_save.side_effect = Exception("unique constraint failed")

    with pytest.raises(Exception) as e:
        book1 = Book(title="Book 1", author="Author 1", category="Category 1", file_path="/path/to/file.pdf")
        book2 = Book(title="Book 2", author="Author 2", category="Category 2", file_path="/path/to/file.pdf")
        book1.save(mock_session)
        book2.save(mock_session)
    assert "unique constraint" in str(e.value)


def test_book_creation_null_values():
    book = Book(title=None, author=None, category=None, cover_image_url=None, file_path="/path/to/file.pdf")
    assert book.title is None
    assert book.author is None
    assert book.category is None
    assert book.cover_image_url is None


def test_book_representation():
    book = Book(title="The Hobbit", author="J.R.R. Tolkien", category="Fantasy", file_path="/path/to/file.pdf")
    assert repr(book) == "<Book(title='The Hobbit', author='J.R.R. Tolkien', category='Fantasy', cover_image_url=None, file_path='/path/to/file.pdf')>"

def test_book_file_path_required():
    with pytest.raises(ValueError) as e:
        book = Book(title="Test Book", author="Test Author", category="Test Category")
    assert "file_path cannot be empty" in str(e.value)


@patch('backend.models.Book.save', autospec=True)
def test_book_file_path_unique(mock_save):
    mock_session = Mock()
    mock_save.side_effect = Exception("unique constraint failed")

    with pytest.raises(Exception) as e:
        book1 = Book(title="Book 1", author="Author 1", category="Category 1", file_path="/path/to/file.pdf")
        book2 = Book(title="Book 2", author="Author 2", category="Category 2", file_path="/path/to/file.pdf")
        book1.save(mock_session)
        book2.save(mock_session)
    assert "unique constraint" in str(e.value)

def test_book_save_success():
    mock_session = Mock()
    book = Book(title="Book 1", author="Author 1", category="Category 1", file_path="/path/to/file.pdf")
    book.save(mock_session)
    mock_session.add.assert_called_once_with(book)
    mock_session.commit.assert_called_once()

def test_book_save_failure():
    mock_session = Mock()
    mock_session.commit.side_effect = Exception("Database error")
    book = Book(title="Book 1", author="Author 1", category="Category 1", file_path="/path/to/file.pdf")
    with pytest.raises(Exception) as e:
        book.save(mock_session)
    assert "Database error" in str(e.value)
    mock_session.add.assert_called_once_with(book)
    mock_session.rollback.assert_called_once()

def test_book_creation_with_long_title():
    long_title = "a" * 256  #Simulate a long title
    book = Book(title=long_title, author="Author 1", category="Category 1", file_path="/path/to/file.pdf")
    assert len(book.title) == 256

def test_book_creation_with_long_author():
    long_author = "a" * 256 #Simulate a long author name
    book = Book(title="Book 1", author=long_author, category="Category 1", file_path="/path/to/file.pdf")
    assert len(book.author) == 256

def test_book_creation_with_long_category():
    long_category = "a" * 256 #Simulate a long category name
    book = Book(title="Book 1", author="Author 1", category=long_category, file_path="/path/to/file.pdf")
    assert len(book.category) == 256

def test_book_creation_with_long_filepath():
    long_filepath = "a" * 512 #Simulate a long filepath, assuming a limit around this number
    with pytest.raises(ValueError) as e:
        book = Book(title="Book 1", author="Author 1", category="Category 1", file_path=long_filepath)
    assert "file_path too long" in str(e.value) # Assuming a validation for filepath length exists.


```