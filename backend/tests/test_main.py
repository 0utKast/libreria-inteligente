import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile, HTTPException
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
    query_rag_endpoint
)
from backend import crud, models, schemas
import io
import os
from tempfile import NamedTemporaryFile
import uuid


@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    return mock_db

@pytest.fixture
def mock_genai():
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '```json\n{"title": "Test Title", "author": "Test Author", "category": "Test Category"}\n```'
    mock_genai = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    return mock_genai


@patch("backend.main.genai")
def test_analyze_with_gemini_success(mock_genai):
    text = "This is a test text."
    result = analyze_with_gemini(text)
    assert result == {"title": "Test Title", "author": "Test Author", "category": "Test Category"}


@patch("backend.main.genai")
def test_analyze_with_gemini_failure(mock_genai):
    mock_genai.GenerativeModel.side_effect = Exception("API error")
    text = "This is a test text."
    result = analyze_with_gemini(text)
    assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}


@patch("backend.main.fitz.open")
def test_process_pdf_success(mock_fitz_open):
    mock_page = MagicMock()
    mock_page.get_text.return_value = "This is a test PDF."
    mock_doc = MagicMock()
    mock_doc.load_page.return_value = mock_page
    mock_doc.__len__.return_value = 1
    mock_fitz_open.return_value = mock_doc
    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        file_path = temp_file.name
    result = process_pdf(file_path, "static/covers")
    os.remove(file_path)
    assert "text" in result
    assert result["text"].startswith("This is a test PDF.")

def test_process_pdf_no_cover():
    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        file_path = temp_file.name
    result = process_pdf(file_path, "static/covers")
    os.remove(file_path)
    assert "text" in result
    assert result["cover_image_url"] is None


@patch("backend.main.epub.read_epub")
def test_process_epub_success(mock_read_epub):
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body>This is a test EPUB.</body></html>"
    mock_book.get_items_of_type.return_value = [mock_item]
    mock_read_epub.return_value = mock_book
    with NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
        file_path = temp_file.name
    result = process_epub(file_path, "static/covers")
    os.remove(file_path)
    assert "text" in result
    assert result["text"].startswith("This is a test EPUB.")



@patch("backend.main.epub.read_epub")
def test_process_epub_no_text(mock_read_epub):
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body></body></html>"
    mock_book.get_items_of_type.return_value = [mock_item]
    mock_read_epub.return_value = mock_book
    with NamedTemporaryFile(suffix=".epub", delete=False) as temp_file:
        file_path = temp_file.name
    with pytest.raises(HTTPException):
        process_epub(file_path, "static/covers")
    os.remove(file_path)


@patch("backend.main.shutil.copyfileobj")
@patch("backend.main.crud.create_book")
@patch("backend.main.analyze_with_gemini")
@patch("backend.main.process_pdf")
@patch("backend.main.crud.get_book_by_path")
@patch("backend.main.os.makedirs")
@patch('backend.main.open', new_callable=mock_open)
def test_upload_book_pdf_success(mock_open, mock_get_book_by_path, mock_process_pdf, mock_analyze_with_gemini, mock_create_book, mock_copyfileobj, mock_makedirs):
    mock_get_book_by_path.return_value = None
    mock_process_pdf.return_value = {"text": "Test text", "cover_image_url": "test.jpg"}
    mock_analyze_with_gemini.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_create_book.return_value = {"id":1, "title": "Test Title", "author": "Test Author", "category": "Test Category", "cover_image_url": "test.jpg", "file_path": "test.pdf"}

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = io.BytesIO(b"test")

    with patch('backend.main.database.SessionLocal') as mock_session:
        result = upload_book(db=mock_session.return_value, book_file=mock_file)
    assert result["title"] == "Test Title"

@patch("backend.main.shutil.copyfileobj")
@patch("backend.main.crud.create_book")
@patch("backend.main.analyze_with_gemini")
@patch("backend.main.process_epub")
@patch("backend.main.crud.get_book_by_path")
@patch("backend.main.os.makedirs")
@patch('backend.main.open', new_callable=mock_open)
def test_upload_book_epub_success(mock_open, mock_get_book_by_path, mock_process_epub, mock_analyze_with_gemini, mock_create_book, mock_copyfileobj, mock_makedirs):
    mock_get_book_by_path.return_value = None
    mock_process_epub.return_value = {"text": "Test text", "cover_image_url": "test.jpg"}
    mock_analyze_with_gemini.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_create_book.return_value = {"id":1, "title": "Test Title", "author": "Test Author", "category": "Test Category", "cover_image_url": "test.jpg", "file_path": "test.epub"}

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.epub"
    mock_file.file = io.BytesIO(b"test")

    with patch('backend.main.database.SessionLocal') as mock_session:
        result = upload_book(db=mock_session.return_value, book_file=mock_file)
    assert result["title"] == "Test Title"


@patch("backend.main.crud.get_books")
def test_read_books(mock_get_books):
    mock_get_books.return_value = [{"id": 1, "title": "Test Book"}]
    books = read_books(db=MagicMock())
    assert len(books) == 1


@patch("backend.main.crud.get_books_count")
def test_get_books_count(mock_get_books_count):
    mock_get_books_count.return_value = 10
    count = get_books_count(db=MagicMock())
    assert count == 10


@patch("backend.main.crud.get_books_by_partial_title")
def test_search_books(mock_get_books_by_partial_title):
    mock_get_books_by_partial_title.return_value = [{"id": 1, "title": "Test Book"}]
    books = search_books(title="Test", db=MagicMock())
    assert len(books) == 1


@patch("backend.main.crud.get_categories")
def test_read_categories(mock_get_categories):
    mock_get_categories.return_value = ["Test Category"]
    categories = read_categories(db=MagicMock())
    assert categories == ["Test Category"]


@patch("backend.main.crud.delete_book")
def test_delete_single_book(mock_delete_book):
    mock_delete_book.return_value = {"id": 1, "title": "Test Book"}
    result = delete_single_book(book_id=1, db=MagicMock())
    assert result == {"message": "Libro 'Test Book' eliminado con éxito."}


@patch("backend.main.crud.delete_books_by_category")
def test_delete_category_and_books(mock_delete_books_by_category):
    mock_delete_books_by_category.return_value = 1
    result = delete_category_and_books(category_name="Test Category", db=MagicMock())
    assert result == {"message": "Categoría 'Test Category' y sus 1 libros han sido eliminados."}


@patch("backend.main.crud.delete_book")
def test_delete_single_book_not_found(mock_delete_book):
    mock_delete_book.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_single_book(book_id=1, db=MagicMock())
    assert excinfo.value.status_code == 404


@patch("backend.main.crud.delete_books_by_category")
def test_delete_category_and_books_not_found(mock_delete_books_by_category):
    mock_delete_books_by_category.return_value = 0
    with pytest.raises(HTTPException) as excinfo:
        delete_category_and_books(category_name="Test Category", db=MagicMock())
    assert excinfo.value.status_code == 404



@patch("backend.main.FileResponse")
@patch("backend.main.crud.delete_book")
def test_download_book(mock_delete_book, mock_fileresp):
    mock_book = MagicMock()
    mock_book.file_path = "test.pdf"
    mock_book.title = "test book"

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    download_book(book_id=1, db=mock_db)
    mock_fileresp.assert_called_once()

@patch("backend.main.FileResponse")
@patch("backend.main.crud.delete_book")
def test_download_book_not_found(mock_delete_book, mock_fileresp):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        download_book(book_id=1, db=mock_db)
    assert excinfo.value.status_code == 404



@pytest.mark.asyncio
@patch("backend.main.convert_epub_to_pdf")
async def test_convert_epub_to_pdf(mock_convert):
    mock_convert.return_value = {"download_url": "/temp_books/test.pdf"}
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test")
    result = await convert_epub_to_pdf(file=mock_file)
    assert result["download_url"] == "/temp_books/test.pdf"



@pytest.mark.asyncio
@patch("backend.main.rag.process_book_for_rag")
async def test_upload_book_for_rag(mock_process_book):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test")
    result = await upload_book_for_rag(file=mock_file)
    assert "book_id" in result
    assert "message" in result

@pytest.mark.asyncio
@patch("backend.main.rag.query_rag")
async def test_query_rag_endpoint(mock_query_rag):
    mock_query_rag.return_value = "Test response"
    query_data = schemas.RagQuery(query="Test query", book_id="test_id")
    result = await query_rag_endpoint(query_data=query_data)
    assert result["response"] == "Test response"

from unittest.mock import mock_open