import pytest
from unittest.mock import Mock, patch
import crud
import models
import os

# Mock para la sesión de SQLAlchemy
mock_session = Mock()
mock_book = Mock(spec=models.Book)
mock_book.file_path = "/tmp/test_file.txt"
mock_book.cover_image_url = "/tmp/test_cover.jpg"
mock_book.id = 1
mock_book.title = "Test Title"
mock_book.author = "Test Author"
mock_book.category = "Test Category"
mock_book.url = "Test URL"

mock_book2 = Mock(spec=models.Book)
mock_book2.file_path = "/tmp/test_file2.txt"
mock_book2.cover_image_url = "/tmp/test_cover2.jpg"
mock_book2.id = 2
mock_book2.title = "Test Title 2"
mock_book2.author = "Test Author 2"
mock_book2.category = "Test Category 2"
mock_book2.url = "Test URL 2"


def test_get_book_by_path():
    mock_session.query().filter().first.side_effect = [mock_book, None, None]
    assert crud.get_book_by_path(mock_session, "/tmp/test_file.txt") == mock_book
    assert crud.get_book_by_path(mock_session, "/tmp/test_file2.txt") is None
    assert crud.get_book_by_path(mock_session, "") is None
    mock_session.query().filter().first.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.get_book_by_path(mock_session, "/tmp/test_file.txt")
    assert str(e.value) == "Database error"


def test_get_book_by_title():
    mock_session.query().filter().first.side_effect = [mock_book, None, None]
    assert crud.get_book_by_title(mock_session, "Test Title") == mock_book
    assert crud.get_book_by_title(mock_session, "Test Title 2") is None
    assert crud.get_book_by_title(mock_session, "") is None
    mock_session.query().filter().first.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.get_book_by_title(mock_session, "Test Title")
    assert str(e.value) == "Database error"


def test_get_books_by_partial_title():
    mock_session.query().filter().offset().limit().all.side_effect = [[mock_book], [], []]
    assert crud.get_books_by_partial_title(mock_session, "Test") == [mock_book]
    assert crud.get_books_by_partial_title(mock_session, "NoMatch") == []
    assert crud.get_books_by_partial_title(mock_session, "") == []
    mock_session.query().filter().offset().limit().all.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.get_books_by_partial_title(mock_session, "Test")
    assert str(e.value) == "Database error"


def test_get_books():
    mock_session.query().order_by().all.side_effect = [[mock_book], [], [mock_book, mock_book2]]
    assert crud.get_books(mock_session) == [mock_book]
    assert crud.get_books(mock_session, category="Test") == [mock_book]
    assert crud.get_books(mock_session, search="Test") == [mock_book]
    assert crud.get_books(mock_session, author="Test") == [mock_book]
    assert crud.get_books(mock_session, category="Test Category 2") == [mock_book2]
    assert crud.get_books(mock_session, limit=1, offset=0) == [mock_book]
    assert crud.get_books(mock_session, limit=1, offset=1) == []
    mock_session.query().order_by().all.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.get_books(mock_session)
    assert str(e.value) == "Database error"


def test_get_categories():
    mock_session.query().distinct().order_by().all.side_effect = [[("Test",), ("Test2",)] ,[]]
    assert crud.get_categories(mock_session) == ["Test", "Test2"]
    assert crud.get_categories(mock_session) == []
    mock_session.query().distinct().order_by().all.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.get_categories(mock_session)
    assert str(e.value) == "Database error"



def test_create_book():
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_book
    assert crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "Test URL", "/tmp/test.txt") == mock_book
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "", "Test Author", "Test Category", "Test URL", "/tmp/test.txt")
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "Test Title", "", "Test Category", "Test URL", "/tmp/test.txt")
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "Test Title", "Test Author", "", "Test URL", "/tmp/test.txt")
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "", "/tmp/test.txt")
    with pytest.raises(ValueError):
        crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "Test URL", "")
    mock_session.add.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.create_book(mock_session, "Test Title", "Test Author", "Test Category", "Test URL", "/tmp/test.txt")
    assert str(e.value) == "Database error"


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
    mock_remove.assert_called_once()
    mock_session.query().filter().first.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.delete_book(mock_session, 1)
    assert str(e.value) == "Database error"


@patch('os.remove')
def test_delete_books_by_category(mock_remove):
    os.makedirs("/tmp", exist_ok=True)
    open("/tmp/test_file.txt", "w").close()
    open("/tmp/test_cover.jpg", "w").close()
    mock_session.query().filter().all.side_effect = [[mock_book], []]
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None
    assert crud.delete_books_by_category(mock_session, "Test Category") == 1
    mock_remove.assert_called()
    assert crud.delete_books_by_category(mock_session, "NoMatch") == 0
    mock_session.query().filter().all.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.delete_books_by_category(mock_session, "Test Category")
    assert str(e.value) == "Database error"


def test_get_books_count():
    mock_session.query().count.side_effect = [1, 0]
    assert crud.get_books_count(mock_session) == 1
    assert crud.get_books_count(mock_session) == 0
    mock_session.query().count.side_effect = Exception("Database error")
    with pytest.raises(Exception) as e:
        crud.get_books_count(mock_session)
    assert str(e.value) == "Database error"