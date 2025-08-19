import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
import crud
import models

@pytest.fixture
def mock_db_session():
    return Mock(spec=Session)

@pytest.fixture
def mock_book():
    return models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path="test.txt")

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_get_book_by_path(mock_os_remove, mock_os_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_path(mock_db_session, "test.txt")
    assert book == mock_book

def test_get_book_by_path_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_path(mock_db_session, "test.txt")
    assert book is None

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_get_book_by_title(mock_os_remove, mock_os_exists, mock_db_session, mock_book):
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
    books = crud.get_books_by_partial_title(mock_db_session, "NonExistent")
    assert len(books) == 0

def test_get_books(mock_db_session, mock_book):
    mock_db_session.query().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session)
    assert len(books) == 1
    assert books[0] == mock_book

def test_get_books_filtered(mock_db_session, mock_book):
    mock_db_session.query().filter().filter().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session, category="Test Category", author="Test Author")
    assert len(books) == 1
    assert books[0] == mock_book

def test_get_categories(mock_db_session):
    mock_db_session.query().distinct().order_by().all.return_value = [("Test Category",)]
    categories = crud.get_categories(mock_db_session)
    assert categories == ["Test Category"]

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_create_book(mock_os_remove, mock_os_exists, mock_db_session):
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None
    book = crud.create_book(mock_db_session, "Test Book", "Test Author", "Test Category", "test.jpg", "test.txt")
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert isinstance(book, models.Book)

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_delete_book(mock_os_remove, mock_os_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    mock_db_session.delete.return_value = None
    mock_db_session.commit.return_value = None
    deleted_book = crud.delete_book(mock_db_session, 1)
    mock_os_remove.assert_called()
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
    assert deleted_book == mock_book

def test_delete_book_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    deleted_book = crud.delete_book(mock_db_session, 1)
    assert deleted_book is None

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_delete_books_by_category(mock_os_remove, mock_os_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().all.return_value = [mock_book]
    mock_db_session.commit.return_value = None
    deleted_count = crud.delete_books_by_category(mock_db_session, "Test Category")
    mock_os_remove.assert_called()
    mock_db_session.commit.assert_called_once()
    assert deleted_count == 1

def test_delete_books_by_category_not_found(mock_db_session):
    mock_db_session.query().filter().all.return_value = []
    deleted_count = crud.delete_books_by_category(mock_db_session, "NonExistent")
    assert deleted_count == 0

def test_get_books_count(mock_db_session):
    mock_db_session.query().count.return_value = 1
    count = crud.get_books_count(mock_db_session)
    assert count == 1

@patch('os.remove', side_effect=OSError)
def test_delete_book_file_error(mock_os_remove, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    with pytest.raises(OSError):
        crud.delete_book(mock_db_session, 1)

@patch('crud.db.query', side_effect=SQLAlchemyError)
def test_crud_functions_database_error(mock_db_query):
    with pytest.raises(SQLAlchemyError):
        crud.get_book_by_path(Mock(spec=Session), "test.txt")
    with pytest.raises(SQLAlchemyError):
        crud.get_book_by_title(Mock(spec=Session), "test")
    with pytest.raises(SQLAlchemyError):
        crud.get_books_by_partial_title(Mock(spec=Session), "test")
    with pytest.raises(SQLAlchemyError):
        crud.get_books(Mock(spec=Session))
    with pytest.raises(SQLAlchemyError):
        crud.get_categories(Mock(spec=Session))
    with pytest.raises(SQLAlchemyError):
        crud.create_book(Mock(spec=Session), "test", "test", "test", "test", "test")
    with pytest.raises(SQLAlchemyError):
        crud.delete_book(Mock(spec=Session), 1)
    with pytest.raises(SQLAlchemyError):
        crud.delete_books_by_category(Mock(spec=Session), "test")
    with pytest.raises(SQLAlchemyError):
        crud.get_books_count(Mock(spec=Session))