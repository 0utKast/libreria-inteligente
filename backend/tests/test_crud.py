import pytest
from unittest.mock import Mock
import crud
import os

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_book():
    return Mock(id=1, title="Book Title", author="Author Name", category="Category", cover_image_url="cover.jpg", file_path="book.pdf")

def test_get_book_by_path(mock_db, mock_book):
    mock_db.query().filter().first.return_value = mock_book
    book = crud.get_book_by_path(mock_db, "book.pdf")
    assert book == mock_book
    mock_db.query().filter().first.assert_called_once_with()

def test_get_book_by_path_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    book = crud.get_book_by_path(mock_db, "nonexistent.pdf")
    assert book is None
    mock_db.query().filter().first.assert_called_once_with()

def test_get_book_by_title(mock_db, mock_book):
    mock_db.query().filter().first.return_value = mock_book
    book = crud.get_book_by_title(mock_db, "Book Title")
    assert book == mock_book
    mock_db.query().filter().first.assert_called_once_with()

def test_get_book_by_title_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    book = crud.get_book_by_title(mock_db, "Nonexistent Title")
    assert book is None
    mock_db.query().filter().first.assert_called_once_with()

def test_get_books_by_partial_title(mock_db, mock_book):
    mock_db.query().filter().offset().limit().all.return_value = [mock_book]
    books = crud.get_books_by_partial_title(mock_db, "Book")
    assert books == [mock_book]
    mock_db.query().filter().offset().limit().all.assert_called_once_with()

def test_get_books_by_partial_title_not_found(mock_db):
    mock_db.query().filter().offset().limit().all.return_value = []
    books = crud.get_books_by_partial_title(mock_db, "Nonexistent")
    assert books == []
    mock_db.query().filter().offset().limit().all.assert_called_once_with()


def test_get_books(mock_db, mock_book):
    mock_db.query().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db)
    assert books == [mock_book]
    mock_db.query().order_by().all.assert_called_once_with()

def test_get_books_with_filters(mock_db, mock_book):
    mock_db.query().filter().filter().filter().order_by().all.return_value = [mock_book]
    books = crud.get_books(mock_db, category="Category", search="Book", author="Author")
    assert books == [mock_book]
    mock_db.query().filter().filter().filter().order_by().all.assert_called_once_with()

def test_get_categories(mock_db):
    mock_db.query().distinct().order_by().all.return_value = [("Category1",), ("Category2",)]
    categories = crud.get_categories(mock_db)
    assert categories == ["Category1", "Category2"]
    mock_db.query().distinct().order_by().all.assert_called_once_with()

def test_create_book(mock_db, mock_book):
    mock_db.add.return_value = None
    mock_db.refresh.return_value = mock_book
    book = crud.create_book(mock_db, "New Book", "New Author", "New Category", "new_cover.jpg", "new_book.pdf")
    assert book == mock_book
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_delete_book(mock_db, mock_book):
    mock_db.query().filter().first.return_value = mock_book
    os.remove = Mock()
    book = crud.delete_book(mock_db, 1)
    assert book == mock_book
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()
    os.remove.assert_called()

def test_delete_book_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    book = crud.delete_book(mock_db, 1)
    assert book is None
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


def test_delete_books_by_category(mock_db, mock_book):
    mock_db.query().filter().all.return_value = [mock_book]
    os.remove = Mock()
    count = crud.delete_books_by_category(mock_db, "Category")
    assert count == 1
    mock_db.delete.assert_called()
    mock_db.commit.assert_called_once()
    os.remove.assert_called()

def test_delete_books_by_category_not_found(mock_db):
    mock_db.query().filter().all.return_value = []
    count = crud.delete_books_by_category(mock_db, "Category")
    assert count == 0
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


def test_get_books_count(mock_db):
    mock_db.query().count.return_value = 5
    count = crud.get_books_count(mock_db)
    assert count == 5
    mock_db.query().count.assert_called_once()
