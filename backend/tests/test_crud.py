import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import crud
import models

@pytest.fixture
def mock_db_session():
    mock_session = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    return mock_session

@pytest.fixture
def mock_book():
    return models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="test_cover.jpg", file_path="test_file.pdf")

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_get_book_by_path(mock_remove, mock_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_path(mock_db_session, "test_file.pdf")
    assert book == mock_book

def test_get_book_by_path_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_path(mock_db_session, "nonexistent_file.pdf")
    assert book is None

def test_get_book_by_title(mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_title(mock_db_session, "Test Book")
    assert book == mock_book

def test_get_book_by_title_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_title(mock_db_session, "Nonexistent Book")
    assert book is None

def test_get_books_by_partial_title(mock_db_session, mock_book):
    mock_db_session.query().filter().offset().limit().all.return_value = [mock_book]
    books = crud.get_books_by_partial_title(mock_db_session, "Test")
    assert len(books) == 1
    assert books[0] == mock_book

def test_get_books_by_partial_title_not_found(mock_db_session):
    mock_db_session.query().filter().offset().limit().all.return_value = []
    books = crud.get_books_by_partial_title(mock_db_session, "Nonexistent")
    assert len(books) == 0

def test_get_books(mock_db_session, mock_book):
    mock_db_session.query().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session)
    assert len(books) == 1
    assert books[0] == mock_book

def test_get_books_filtered(mock_db_session, mock_book):
    mock_db_session.query().filter().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session, category="Test Category", author="Test Author")
    assert len(books) == 1
    assert books[0] == mock_book

def test_get_categories(mock_db_session):
    mock_db_session.query().distinct().order_by().all.return_value = [("Test Category",)]
    categories = crud.get_categories(mock_db_session)
    assert categories == ["Test Category"]

def test_create_book(mock_db_session):
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    book = crud.create_book(mock_db_session, "New Book", "New Author", "New Category", "new_cover.jpg", "new_file.pdf")
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert isinstance(book, models.Book)

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_delete_book(mock_remove, mock_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    deleted_book = crud.delete_book(mock_db_session, 1)
    mock_remove.assert_called()
    mock_db_session.delete.assert_called_once_with(mock_book)
    mock_db_session.commit.assert_called_once()
    assert deleted_book == mock_book

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    deleted_book = crud.delete_book(mock_db_session, 1)
    assert deleted_book is None

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_delete_books_by_category(mock_remove, mock_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().all.return_value = [mock_book]
    count = crud.delete_books_by_category(mock_db_session, "Test Category")
    mock_remove.assert_called()
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
    assert count == 1

def test_delete_books_by_category_not_found(mock_db_session):
    mock_db_session.query().filter().all.return_value = []
    count = crud.delete_books_by_category(mock_db_session, "Nonexistent Category")
    assert count == 0

def test_get_books_count(mock_db_session):
    mock_db_session.query().count.return_value = 5
    count = crud.get_books_count(mock_db_session)
    assert count == 5

def test_get_books_sqlalchemy_error(mock_db_session):
    mock_db_session.query().filter.side_effect = SQLAlchemyError("Database error")
    with pytest.raises(SQLAlchemyError):
        crud.get_books(mock_db_session)

```