import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from backend.main import (
    app,
    analyze_with_gemini,
    process_pdf,
    process_epub,
    upload_book,
    read_books,
    get_books_count,
    search_books,
    read_categories,
    delete_single_book,
    delete_category_and_books,
    download_book,
    convert_epub_to_pdf,
    upload_book_for_rag,
    query_rag_endpoint,
)
from backend import crud, models, schemas
from io import BytesIO
import uuid

# Mocks para dependencias externas
mock_genai = MagicMock()
mock_crud = MagicMock()
mock_database = MagicMock()
mock_db = MagicMock()
mock_db.query = MagicMock(return_value=MagicMock(filter=MagicMock(return_value=MagicMock(first=MagicMock()))))


@pytest.fixture
def mock_genai_fixture():
    with patch('backend.main.genai', mock_genai):
        yield

@pytest.fixture
def mock_crud_fixture():
    with patch('backend.main.crud', mock_crud):
        yield

@pytest.fixture
def mock_database_fixture():
    with patch('backend.main.database', mock_database):
        mock_database.SessionLocal = MagicMock(return_value=mock_db)
        yield

@pytest.fixture
def mock_file():
    file_mock = MagicMock()
    file_mock.filename = "test.pdf"
    file_mock.file = BytesIO(b"test")
    file_mock.read = AsyncMock(return_value=b"test")
    return file_mock


@pytest.mark.asyncio
async def test_analyze_with_gemini_success(mock_genai_fixture):
    mock_model = AsyncMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_model.generate_content_async.return_value = AsyncMock(text='{"title": "Test", "author": "Author", "category": "Category"}')
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Test", "author": "Author", "category": "Category"}

@pytest.mark.asyncio
async def test_analyze_with_gemini_error(mock_genai_fixture):
    mock_model = AsyncMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_model.generate_content_async.side_effect = Exception("Gemini Error")
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}


def test_process_pdf_success():
    with patch('backend.main.fitz.open', return_value=MagicMock(load_page=MagicMock(return_value=MagicMock(get_text=MagicMock(return_value="test"))))):
        result = process_pdf("test.pdf", "static/covers")
        assert "text" in result
        assert "cover_image_url" in result


def test_process_epub_success():
    book = MagicMock()
    book.get_items_of_type = MagicMock(return_value=[MagicMock(get_content=MagicMock(return_value="<html>test</html>"))])
    with patch('backend.main.epub.read_epub', return_value=book):
        result = process_epub("test.epub", "static/covers")
        assert "text" in result
        assert "cover_image_url" in result

@pytest.mark.asyncio
@pytest.mark.parametrize("file_ext, expected_status", [(".pdf", 200), (".epub", 200), (".txt", 400)])
async def test_upload_book(mock_crud_fixture, mock_database_fixture, mock_file, file_ext, expected_status):
    mock_file.filename = f"test{file_ext}"
    mock_crud.get_book_by_path.return_value = None
    mock_crud.create_book.return_value = schemas.Book(id=1, title="Test", author="Test Author")
    with patch("backend.main.analyze_with_gemini", AsyncMock(return_value={"title": "Test", "author": "Test Author", "category": "Test Category"})):
        if expected_status == 200:
            response = await upload_book(db=mock_db, book_file=mock_file)
            assert response.title == "Test"
        else:
            with pytest.raises(HTTPException) as e:
                await upload_book(db=mock_db, book_file=mock_file)
                assert e.value.status_code == expected_status



def test_read_books(mock_crud_fixture, mock_database_fixture):
    mock_crud.get_books.return_value = [schemas.Book(id=1, title="Test")]
    books = read_books(db=mock_db)
    assert len(books) == 1

def test_get_books_count(mock_crud_fixture, mock_database_fixture):
    mock_crud.get_books_count.return_value = 10
    count = get_books_count(db=mock_db)
    assert count == 10

def test_search_books(mock_crud_fixture, mock_database_fixture):
    mock_crud.get_books_by_partial_title.return_value = [schemas.Book(id=1, title="Test")]
    books = search_books(title="Test", db=mock_db)
    assert len(books) == 1

def test_read_categories(mock_crud_fixture, mock_database_fixture):
    mock_crud.get_categories.return_value = ["Category 1", "Category 2"]
    categories = read_categories(db=mock_db)
    assert len(categories) == 2

def test_delete_single_book(mock_crud_fixture, mock_database_fixture):
    mock_crud.delete_book.return_value = schemas.Book(id=1, title="Test")
    response = delete_single_book(book_id=1, db=mock_db)
    assert response["message"] == "Libro 'Test' eliminado con éxito."

def test_delete_category_and_books(mock_crud_fixture, mock_database_fixture):
    mock_crud.delete_books_by_category.return_value = 5
    response = delete_category_and_books(category_name="Test", db=mock_db)
    assert response["message"] == "Categoría 'Test' y sus 5 libros han sido eliminados."

def test_download_book(mock_crud_fixture, mock_database_fixture):
    mock_db.query.return_value.filter.return_value.first.return_value = models.Book(id=1, title="Test", file_path="test.pdf")
    with patch('backend.main.FileResponse') as mock_fileresp:
        download_book(book_id=1, db=mock_db)
        mock_fileresp.assert_called()


@pytest.mark.asyncio
async def test_convert_epub_to_pdf_success():
    mock_file = MagicMock()
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test")
    with patch('backend.main.uuid.uuid4', return_value="test_uuid"):
        with patch('backend.main.open', mock_open=MagicMock()):
            response = await convert_epub_to_pdf(file=mock_file)
            assert response["download_url"] == "/temp_books/test_uuid.pdf"

@pytest.mark.asyncio
async def test_upload_book_for_rag(mock_crud_fixture, mock_database_fixture, mock_file):
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test")
    with patch('backend.main.rag.process_book_for_rag', AsyncMock()):
        with patch('backend.main.uuid.uuid4', return_value="test_uuid"):
            response = await upload_book_for_rag(file=mock_file)
            assert response["book_id"] == "test_uuid"


@pytest.mark.asyncio
async def test_query_rag_endpoint():
    with patch('backend.main.rag.query_rag', AsyncMock(return_value="test response")):
        response = await query_rag_endpoint(schemas.RagQuery(query="test", book_id="test_id"))
        assert response["response"] == "test response"