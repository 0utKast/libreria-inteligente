import pytest
from unittest.mock import Mock, patch
import crud
import models
import os

# Mock para la sesión de SQLAlchemy
mock_session = Mock()
mock_book = Mock(spec=models.Book)

# Mocks para los archivos.  Asumiendo que file_path y cover_image_url son rutas de archivo.
mock_book.file_path = "/tmp/test_file.txt"
mock_book.cover_image_url = "/tmp/test_cover.jpg"
mock_book.id = 1
mock_book2 = Mock(spec=models.Book)
mock_book2.file_path = "/tmp/test_file2.txt"
mock_book2.cover_image_url = "/tmp/test_cover2.jpg"
mock_book2.id = 2


def test_get_book_by_path():
    mock_session.query().filter().first.side_effect = [mock_book, None]
    assert crud.get_book_by_path(mock_session, "/tmp/test_file.txt") == mock_book
    assert crud.get_book_by_path(mock_session, "/tmp/test_file2.txt") is None
    assert crud.get_book_by_path(mock_session, "") is None


def test_get_book_by_title():
    mock_session.query().filter().first.side_effect = [mock_book, None]
    assert crud.get_book_by_title(mock_session, "Test Title") == mock_book
    assert crud.get_book_by_title(mock_session, "Test Title 2") is None
    assert crud.get_book_by_title(mock_session, "") is None


def test_get_books_by_partial_title():
    mock_session.query().filter().offset().limit().all.side_effect = [[mock_book], []]
    assert crud.get_books_by_partial_title(mock_session, "Test") == [mock_book]
    assert crud.get_books_by_partial_title(mock_session, "NoMatch") == []
    assert crud.get_books_by_partial_title(mock_session, "") == []


def test_get_books():
    mock_session.query().order_by().all.side_effect = [[mock_book], []]
    assert crud.get_books(mock_session) == [mock_book]
    assert crud.get_books(mock_session, category="Test") == [mock_book]
    assert crud.get_books(mock_session, search="Test") == [mock_book]
    assert crud.get_books(mock_session, author="Test") == [mock_book]
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
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "", "Test Author", "Test Category", "Test URL", "/tmp/test.txt")


@patch('os.remove')
def test_delete_book(mock_remove):
    os.makedirs("/tmp", exist_ok=True)
    open("/tmp/test_file.txt", "w").close()
    open("/tmp/test_cover.jpg", "w").close()
    mock_session.query().filter().first.side_effect = [mock_book, None]
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    assert crud.delete_book(mock_session, 1) == mock_book
    mock_remove.assert_called()
    assert crud.delete_book(mock_session, 2) is None


@patch('os.remove')
def test_delete_books_by_category(mock_remove):
    os.makedirs("/tmp", exist_ok=True)
    open("/tmp/test_file.txt", "w").close()
    open("/tmp/test_cover.jpg", "w").close()
    mock_session.query().filter().all.side_effect = [[mock_book], []]
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    assert crud.delete_books_by_category(mock_session, "Test") == 1
    mock_remove.assert_called()
    assert crud.delete_books_by_category(mock_session, "NoMatch") == 0


def test_get_books_count():
    mock_session.query().count.side_effect = [1, 0]
    assert crud.get_books_count(mock_session) == 1
    assert crud.get_books_count(mock_session) == 0