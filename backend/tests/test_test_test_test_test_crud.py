import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import crud
import models

# Mock de la sesión de la base de datos
@pytest.fixture
def mock_db_session():
    mock_session = MagicMock(spec=Session)
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    return mock_session

# Mock de un libro
@pytest.fixture
def mock_book():
    return models.Book(id=1, title="Book Title", author="Author Name", category="Category", cover_image_url="cover.jpg", file_path="book.pdf")

#Mocks para os.path.exists y os.remove
@patch('os.path.exists')
@patch('os.remove')
def test_delete_book(mock_remove, mock_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    mock_exists.return_value = True
    crud.delete_book(mock_db_session, 1)
    mock_db_session.delete.assert_called_once_with(mock_book)
    mock_db_session.commit.assert_called_once()
    mock_remove.assert_called_once_with("book.pdf")

@patch('os.path.exists')
@patch('os.remove')
def test_delete_book_not_exists(mock_remove, mock_exists, mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    crud.delete_book(mock_db_session, 1)
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()
    mock_remove.assert_not_called()

@patch('os.path.exists')
@patch('os.remove')
def test_delete_book_file_not_exists(mock_remove, mock_exists, mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    mock_exists.return_value = False
    crud.delete_book(mock_db_session, 1)
    mock_db_session.delete.assert_called_once_with(mock_book)
    mock_db_session.commit.assert_called_once()
    mock_remove.assert_not_called()

@patch('os.path.exists')
@patch('os.remove')
def test_delete_books_by_category(mock_remove, mock_exists, mock_db_session, mock_book):
    mock_books = [mock_book, models.Book(id=2, title="Book2", author="Author2", category="Category", cover_image_url="cover2.jpg", file_path="book2.pdf")]
    mock_db_session.query().filter().all.return_value = mock_books
    mock_exists.return_value = True
    deleted_count = crud.delete_books_by_category(mock_db_session, "Category")
    assert deleted_count == 2
    mock_db_session.delete.assert_has_calls([pytest.approx(mock_book), pytest.approx(mock_books[1])])
    mock_db_session.commit.assert_called_once()
    mock_remove.assert_has_calls([pytest.approx("book.pdf"), pytest.approx("book2.pdf")])

def test_delete_books_by_category_empty(mock_db_session):
    mock_db_session.query().filter().all.return_value = []
    deleted_count = crud.delete_books_by_category(mock_db_session, "Category")
    assert deleted_count == 0
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()

def test_get_books_count(mock_db_session):
    mock_db_session.query().count.return_value = 10
    count = crud.get_books_count(mock_db_session)
    assert count == 10

def test_get_categories(mock_db_session):
    mock_db_session.query().distinct().order_by().all.return_value = [("Category1",), ("Category2",)]
    categories = crud.get_categories(mock_db_session)
    assert categories == ["Category1", "Category2"]

def test_get_books(mock_db_session, mock_book):
    mock_db_session.query().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db_session)
    assert books == [mock_book]

def test_get_books_empty(mock_db_session):
    mock_db_session.query().order_by().all.return_value = []
    books = crud.get_books(mock_db_session)
    assert books == []

def test_get_books_by_partial_title(mock_db_session, mock_book):
    mock_db_session.query().filter().offset().limit().all.return_value = [mock_book]
    books = crud.get_books_by_partial_title(mock_db_session, "Book")
    assert books == [mock_book]

def test_get_books_by_partial_title_empty(mock_db_session):
    mock_db_session.query().filter().offset().limit().all.return_value = []
    books = crud.get_books_by_partial_title(mock_db_session, "Book")
    assert books == []

def test_get_book_by_title(mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_title(mock_db_session, "Book Title")
    assert book == mock_book

def test_get_book_by_title_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_title(mock_db_session, "Book Title")
    assert book is None

def test_get_book_by_path(mock_db_session, mock_book):
    mock_db_session.query().filter().first.return_value = mock_book
    book = crud.get_book_by_path(mock_db_session, "book.pdf")
    assert book == mock_book

def test_get_book_by_path_not_found(mock_db_session):
    mock_db_session.query().filter().first.return_value = None
    book = crud.get_book_by_path(mock_db_session, "book.pdf")
    assert book is None

def test_create_book(mock_db_session):
    new_book = crud.create_book(mock_db_session, "New Book", "Author", "Category", "cover.jpg", "book.pdf")
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert isinstance(new_book, models.Book)


def test_create_book_exception(mock_db_session):
    mock_db_session.add.side_effect = SQLAlchemyError("DB error")
    with pytest.raises(SQLAlchemyError):
        crud.create_book(mock_db_session, "New Book", "Author", "Category", "cover.jpg", "book.pdf")

def test_create_book_empty_title(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "", "Author", "Category", "cover.jpg", "book.pdf")

def test_create_book_empty_author(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "Title", "", "Category", "cover.jpg", "book.pdf")

def test_create_book_empty_category(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "Title", "Author", "", "cover.jpg", "book.pdf")

def test_create_book_empty_cover(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "Title", "Author", "Category", "", "book.pdf")

def test_create_book_empty_path(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "Title", "Author", "Category", "cover.jpg", "")

def test_create_book_invalid_cover_url(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "Title", "Author", "Category", "invalid_url", "book.pdf")


def test_create_book_invalid_file_path(mock_db_session):
    with pytest.raises(ValueError):
        crud.create_book(mock_db_session, "Title", "Author", "Category", "cover.jpg", "invalid/path/book.pdf")