import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import crud
import os

# Mock de la sesión de SQLAlchemy
mock_session = Mock(spec=Session)
mock_book = Mock()
mock_book.id = 1
mock_book.file_path = "/tmp/test.txt"
mock_book.cover_image_url = "/tmp/cover.jpg"
mock_book.title = "Test Book"
mock_book.author = "Test Author"
mock_book.category = "Test Category"
mock_book.url = "Test URL"

mock_book_2 = Mock()
mock_book_2.id = 2
mock_book_2.file_path = "/tmp/test2.txt"
mock_book_2.cover_image_url = "/tmp/cover2.jpg"
mock_book_no_files = Mock()
mock_book_no_files.id = 3
mock_book_no_path = Mock()
mock_book_no_path.id = 4
mock_book_no_cover = Mock()
mock_book_no_cover.id = 5
mock_book_no_cover.file_path = "/tmp/test5.txt"
mock_book_no_title = Mock()
mock_book_no_title.id = 6


def test_get_book_by_path():
    mock_session.query().filter().first.side_effect = [mock_book, None, None, None]
    assert crud.get_book_by_path(mock_session, "/tmp/test.txt") == mock_book
    assert crud.get_book_by_path(mock_session, "/tmp/nonexistent.txt") is None
    assert crud.get_book_by_path(mock_session, "") is None
    assert crud.get_book_by_path(mock_session, None) is None


def test_get_book_by_title():
    mock_session.query().filter().first.side_effect = [mock_book, None, None, None]
    assert crud.get_book_by_title(mock_session, "Test Book") == mock_book
    assert crud.get_book_by_title(mock_session, "Nonexistent Book") is None
    assert crud.get_book_by_title(mock_session, "") is None
    assert crud.get_book_by_title(mock_session, None) is None


def test_get_books_by_partial_title():
    mock_session.query().filter().offset().limit().all.side_effect = [[mock_book], [], [], []]
    assert crud.get_books_by_partial_title(mock_session, "Test") == [mock_book]
    assert crud.get_books_by_partial_title(mock_session, "Nonexistent") == []
    assert crud.get_books_by_partial_title(mock_session, "") == []
    assert crud.get_books_by_partial_title(mock_session, None) == []


def test_get_books():
    mock_session.query().filter().order_by().all.side_effect = [[mock_book], []]
    assert crud.get_books(mock_session) == [mock_book]
    assert crud.get_books(mock_session, category="Test") == [mock_book]
    assert crud.get_books(mock_session, author="Test") == [mock_book]
    assert crud.get_books(mock_session, search="Test") == [mock_book]
    assert crud.get_books(mock_session) == []


def test_get_categories():
    mock_session.query().distinct().order_by().all.side_effect = [[("Test",)], []]
    assert crud.get_categories(mock_session) == ["Test"]
    assert crud.get_categories(mock_session) == []


def test_create_book():
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_book
    assert crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "Test URL", "/tmp/test.txt") == mock_book
    assert crud.create_book(mock_session, "", "Test Author", "Test Category", "Test URL", "/tmp/test.txt") == mock_book
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "Test URL", "")
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "", "/tmp/test.txt")


@patch('os.remove')
def test_delete_book(mock_remove):
    mock_remove.return_value = None
    mock_session.query().filter().first.side_effect = [mock_book, None, None, mock_book_no_files, mock_book_no_path, mock_book_no_cover]
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/test.txt", "w") as f:
        f.write("test")
    with open("/tmp/cover.jpg", "w") as f:
        f.write("test")
    assert crud.delete_book(mock_session, 1) == mock_book
    assert not os.path.exists("/tmp/test.txt")
    assert not os.path.exists("/tmp/cover.jpg")
    assert crud.delete_book(mock_session, 2) is None
    assert crud.delete_book(mock_session, None) is None
    assert crud.delete_book(mock_session, 3) == mock_book_no_files
    assert crud.delete_book(mock_session, 4) == mock_book_no_path
    assert crud.delete_book(mock_session, 5) == mock_book_no_cover


@patch('os.remove')
def test_delete_books_by_category(mock_remove):
    mock_remove.return_value = None
    mock_session.query().filter().all.side_effect = [[mock_book], []]
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/test.txt", "w") as f:
        f.write("test")
    assert crud.delete_books_by_category(mock_session, "Test") == 1
    assert not os.path.exists("/tmp/test.txt")
    assert crud.delete_books_by_category(mock_session, "Nonexistent") == 0
    assert crud.delete_books_by_category(mock_session, None) == 0


def test_get_books_count():
    mock_session.query().count.side_effect = [1, 0]
    assert crud.get_books_count(mock_session) == 1
    assert crud.get_books_count(mock_session) == 0


@patch('os.remove')
def test_delete_book_file_error(mock_remove):
    mock_remove.side_effect = OSError
    mock_session.query().filter().first.return_value = mock_book
    mock_session.delete.return_value = None
    mock_session.commit.side_effect = SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        crud.delete_book(mock_session, 1)


@patch('os.remove')
def test_delete_books_by_category_file_error(mock_remove):
    mock_remove.side_effect = OSError
    mock_session.query().filter().all.return_value = [mock_book]
    mock_session.delete.return_value = None
    mock_session.commit.side_effect = SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        crud.delete_books_by_category(mock_session, "Test")
