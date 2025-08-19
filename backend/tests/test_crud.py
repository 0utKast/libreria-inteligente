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
    return models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path="test.pdf")


def test_get_book_by_path(mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_path(mock_db_session, "test.pdf")
    assert book == mock_book

def test_get_book_by_path_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_path(mock_db_session, "test.pdf")
    assert book is None

def test_get_book_by_title(mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_title(mock_db_session, "Test Book")
    assert book == mock_book

def test_get_book_by_title_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_title(mock_db_session, "Test Book")
    assert book is None

def test_get_books_by_partial_title(mock_db_session, mock_book):
    mock_db_session.query().filter().offset().limit().all.return_value = [mock_book]
    books = crud.get_books_by_partial_title(mock_db_session, "Test")
    assert len(books) == 1
    assert books[0] == mock_book


def test_get_books_by_partial_title_not_found(mock_db_session):
    mock_db_session.query().filter().offset().limit().all.return_value = []
    books = crud.get_books_by_partial_title(mock_db_session, "Test")
    assert len(books) == 0

def test_get_books(mock_db_session, mock_book):
    mock_db_session.query().filter().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session)
    assert len(books) == 1
    assert books[0] == mock_book

def test_get_books_filtered(mock_db_session, mock_book):
    mock_db_session.query().filter().filter().filter().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session, category="Test Category", author="Test Author", search="Test")
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
    book = crud.create_book(mock_db_session, "Test Book", "Test Author", "Test Category", "test.jpg", "test.pdf")
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert isinstance(book, models.Book)

@patch('os.remove')
def test_delete_book(mock_os_remove, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    crud.delete_book(mock_db_session, 1)
    mock_db_session.delete.assert_called_once_with(mock_book)
    mock_db_session.commit.assert_called_once()
    mock_os_remove.assert_called()

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.delete_book(mock_db_session, 1)
    assert book is None

@patch('os.remove')
def test_delete_books_by_category(mock_os_remove, mock_db_session, mock_book):
    mock_db_session.query().filter().all.return_value = [mock_book]
    count = crud.delete_books_by_category(mock_db_session, "Test Category")
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_os_remove.assert_called()
    assert count == 1

def test_delete_books_by_category_not_found(mock_db_session):
    mock_db_session.query().filter().all.return_value = []
    count = crud.delete_books_by_category(mock_db_session, "Test Category")
    assert count == 0


def test_get_books_count(mock_db_session):
    mock_db_session.query().count.return_value = 10
    count = crud.get_books_count(mock_db_session)
    assert count == 10

def test_delete_book_file_error(mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    with patch('os.remove') as mock_remove:
        mock_remove.side_effect = OSError("File not found")
        crud.delete_book(mock_db_session, 1)
        mock_db_session.delete.assert_called_once()
        mock_db_session.commit.assert_called_once()


def test_delete_books_by_category_db_error(mock_db_session, mock_book):
    mock_db_session.query().filter().all.return_value = [mock_book]
    with pytest.raises(SQLAlchemyError):
        with patch.object(mock_db_session, 'commit', side_effect=SQLAlchemyError("Database error")):
            crud.delete_books_by_category(mock_db_session, "Test Category")
