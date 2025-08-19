import pytest
from unittest.mock import Mock
from backend.models import Book

def test_book_creation():
    book = Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", category="Science Fiction", cover_image_url="some_url", file_path="/path/to/book.pdf")
    assert book.title == "The Hitchhiker's Guide to the Galaxy"
    assert book.author == "Douglas Adams"
    assert book.category == "Science Fiction"
    assert book.cover_image_url == "some_url"
    assert book.file_path == "/path/to/book.pdf"

def test_book_creation_no_cover_image():
    book = Book(title="The Lord of the Rings", author="J.R.R. Tolkien", category="Fantasy", file_path="/path/to/book.pdf")
    assert book.cover_image_url is None

def test_book_creation_empty_title():
    with pytest.raises(Exception) as e:  # Expect an error because of missing title
        Book(title="", author="Author", category="Category", file_path="/path/to/file.pdf")
    assert "title can't be empty" in str(e.value) #Customize this to match your validation error message

def test_book_creation_empty_author():
    with pytest.raises(Exception) as e: # Expect an error because of missing author
        Book(title="Title", author="", category="Category", file_path="/path/to/file.pdf")
    assert "author can't be empty" in str(e.value) #Customize this to match your validation error message

def test_book_creation_empty_category():
    with pytest.raises(Exception) as e: # Expect an error because of missing category
        Book(title="Title", author="Author", category="", file_path="/path/to/file.pdf")
    assert "category can't be empty" in str(e.value) #Customize this to match your validation error message


def test_book_creation_duplicate_file_path():
    # Mocking the database interaction to simulate a duplicate file_path
    mock_session = Mock()
    mock_query = Mock()
    mock_query.filter_by.return_value.one_or_none.return_value = Book(file_path="/path/to/book.pdf")
    mock_session.query.return_value = mock_query
    with pytest.raises(Exception) as e:
        Book(title="Title", author="Author", category="Category", file_path="/path/to/book.pdf", session = mock_session)
    assert "File path already exists" in str(e.value)  # Customize to match your error message

def test_book_creation_invalid_file_path():
    with pytest.raises(Exception) as e:
        Book(title="Title", author="Author", category="Category", file_path=123) # Invalid file path type
    assert "Invalid file path format" in str(e.value) # Customize to match your error message


def test_book_representation():
    book = Book(title="Test Book", author="Test Author", category="Test Category", file_path="/path/to/test.pdf")
    assert str(book) == f"Book(title='Test Book', author='Test Author', category='Test Category', file_path='/path/to/test.pdf')"

```