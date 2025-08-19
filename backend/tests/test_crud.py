import pytest
from unittest.mock import Mock
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


def test_get_book_by_path():
    mock_session.query().filter().first.return_value = mock_book
    assert crud.get_book_by_path(mock_session, "/tmp/test.txt") == mock_book
    mock_session.query().filter().first.return_value = None
    assert crud.get_book_by_path(mock_session, "/tmp/nonexistent.txt") is None


def test_get_book_by_title():
    mock_session.query().filter().first.return_value = mock_book
    assert crud.get_book_by_title(mock_session, "Test Book") == mock_book
    mock_session.query().filter().first.return_value = None
    assert crud.get_book_by_title(mock_session, "Nonexistent Book") is None


def test_get_books_by_partial_title():
    mock_session.query().filter().offset().limit().all.return_value = [mock_book]
    assert crud.get_books_by_partial_title(mock_session, "Test") == [mock_book]
    mock_session.query().filter().offset().limit().all.return_value = []
    assert crud.get_books_by_partial_title(mock_session, "Nonexistent") == []


def test_get_books():
    mock_session.query().filter().order_by().all.return_value = [mock_book]
    assert crud.get_books(mock_session) == [mock_book]
    assert crud.get_books(mock_session, category="Test") == [mock_book]
    assert crud.get_books(mock_session, author="Test") == [mock_book]
    assert crud.get_books(mock_session, search="Test") == [mock_book]
    mock_session.query().filter().order_by().all.return_value = []
    assert crud.get_books(mock_session) == []


def test_get_categories():
    mock_session.query().distinct().order_by().all.return_value = [("Test",)]
    assert crud.get_categories(mock_session) == ["Test"]
    mock_session.query().distinct().order_by().all.return_value = []
    assert crud.get_categories(mock_session) == []


def test_create_book():
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_book
    assert crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "Test URL", "/tmp/test.txt") == mock_book


def test_delete_book():
    mock_session.query().filter().first.return_value = mock_book
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

    mock_session.query().filter().first.return_value = None
    assert crud.delete_book(mock_session, 2) is None


def test_delete_books_by_category():
    mock_session.query().filter().all.return_value = [mock_book]
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/test.txt", "w") as f:
        f.write("test")
    assert crud.delete_books_by_category(mock_session, "Test") == 1
    assert not os.path.exists("/tmp/test.txt")
    mock_session.query().filter().all.return_value = []
    assert crud.delete_books_by_category(mock_session, "Nonexistent") == 0


def test_get_books_count():
    mock_session.query().count.return_value = 1
    assert crud.get_books_count(mock_session) == 1

def test_delete_book_file_error():
    mock_session.query().filter().first.return_value = mock_book
    mock_session.delete.return_value = None
    mock_session.commit.side_effect = SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        crud.delete_book(mock_session, 1)

def test_delete_books_by_category_file_error():
    mock_session.query().filter().all.return_value = [mock_book]
    mock_session.delete.return_value = None
    mock_session.commit.side_effect = SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        crud.delete_books_by_category(mock_session, "Test")
