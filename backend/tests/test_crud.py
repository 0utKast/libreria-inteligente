import pytest
from unittest.mock import Mock
import crud
import models

# Mock para la sesión de SQLAlchemy
mock_session = Mock()
mock_book = Mock(spec=models.Book)

#Mocks para los archivos.  Asumiendo que file_path y cover_image_url son rutas de archivo.
mock_book.file_path = "/tmp/test_file.txt"
mock_book.cover_image_url = "/tmp/test_cover.jpg"


def test_get_book_by_path():
    mock_session.query().filter().first.return_value = mock_book
    assert crud.get_book_by_path(mock_session, "/tmp/test_file.txt") == mock_book
    mock_session.query().filter().first.return_value = None
    assert crud.get_book_by_path(mock_session, "/tmp/test_file2.txt") is None

def test_get_book_by_title():
    mock_session.query().filter().first.return_value = mock_book
    assert crud.get_book_by_title(mock_session, "Test Title") == mock_book
    mock_session.query().filter().first.return_value = None
    assert crud.get_book_by_title(mock_session, "Test Title 2") is None

def test_get_books_by_partial_title():
    mock_session.query().filter().offset().limit().all.return_value = [mock_book]
    assert crud.get_books_by_partial_title(mock_session, "Test") == [mock_book]
    mock_session.query().filter().offset().limit().all.return_value = []
    assert crud.get_books_by_partial_title(mock_session, "NoMatch") == []

def test_get_books():
    mock_session.query().order_by().all.return_value = [mock_book]
    assert crud.get_books(mock_session) == [mock_book]
    assert crud.get_books(mock_session, category="Test") == [mock_book]
    assert crud.get_books(mock_session, search="Test") == [mock_book]
    assert crud.get_books(mock_session, author="Test") == [mock_book]
    mock_session.query().order_by().all.return_value = []
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
    import os
    os.makedirs("/tmp", exist_ok=True)
    open("/tmp/test_file.txt", "w").close()
    open("/tmp/test_cover.jpg", "w").close()
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    assert crud.delete_book(mock_session, 1) == mock_book
    mock_session.query().filter().first.return_value = None
    assert crud.delete_book(mock_session, 2) is None

def test_delete_books_by_category():
    mock_session.query().filter().all.return_value = [mock_book]
    import os
    os.makedirs("/tmp", exist_ok=True)
    open("/tmp/test_file.txt", "w").close()
    open("/tmp/test_cover.jpg", "w").close()
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    assert crud.delete_books_by_category(mock_session, "Test") == 1
    mock_session.query().filter().all.return_value = []
    assert crud.delete_books_by_category(mock_session, "NoMatch") == 0


def test_get_books_count():
    mock_session.query().count.return_value = 1
    assert crud.get_books_count(mock_session) == 1
    mock_session.query().count.return_value = 0
    assert crud.get_books_count(mock_session) == 0