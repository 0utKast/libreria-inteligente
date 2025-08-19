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
    query_rag_endpoint,
)
from io import BytesIO
import json
import os


@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.close = MagicMock()
    return mock_db


@pytest.mark.asyncio
@patch("backend.main.genai.GenerativeModel")
async def test_analyze_with_gemini_success(mock_genai):
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '{"title": "Title", "author": "Author", "category": "Category"}'
    mock_genai.return_value = mock_model
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Title", "author": "Author", "category": "Category"}


@pytest.mark.asyncio
@patch("backend.main.genai.GenerativeModel")
async def test_analyze_with_gemini_error(mock_genai):
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("Gemini error")
    mock_genai.return_value = mock_model
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}


@patch("backend.main.fitz.open")
def test_process_pdf_success(mock_fitz_open):
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "test text"
    mock_doc.load_page.return_value = mock_page
    mock_doc.__len__.return_value = 5
    mock_fitz_open.return_value = mock_doc
    mock_pix = MagicMock()
    mock_pix.width = 400
    mock_pix.height = 400
    mock_doc.get_page_images.return_value = [(1, mock_pix)]
    mock_pix.save = MagicMock()

    result = process_pdf("test.pdf", "static/covers")
    assert "text" in result
    assert "cover_image_url" in result


def test_process_pdf_no_cover():
    with patch("backend.main.fitz.open") as mock_fitz_open:
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "test text"
        mock_doc.load_page.return_value = mock_page
        mock_doc.__len__.return_value = 5
        mock_fitz_open.return_value = mock_doc
        mock_doc.get_page_images.return_value = []

        result = process_pdf("test.pdf", "static/covers")
        assert "text" in result
        assert "cover_image_url" not in result or result["cover_image_url"] is None



@patch("backend.main.epub.read_epub")
def test_process_epub_success(mock_read_epub):
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body>Test text</body></html>"
    mock_book.get_items_of_type.return_value = [mock_item]
    mock_read_epub.return_value = mock_book

    result = process_epub("test.epub", "static/covers")
    assert "text" in result
    assert "cover_image_url" in result

@patch("backend.main.epub.read_epub")
def test_process_epub_no_cover(mock_read_epub):
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body>Test text</body></html>"
    mock_book.get_items_of_type.side_effect = [[],[]]

    mock_read_epub.return_value = mock_book

    result = process_epub("test.epub", "static/covers")
    assert "text" in result
    assert "cover_image_url" not in result or result["cover_image_url"] is None


@patch("backend.main.crud.create_book")
@patch("backend.main.process_pdf")
@patch("backend.main.analyze_with_gemini")
@patch("backend.main.crud.get_book_by_path")
@pytest.mark.asyncio
async def test_upload_book_success(mock_get_book, mock_analyze, mock_process, mock_create, mock_db):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = BytesIO(b"test data")
    mock_get_book.return_value = None
    mock_analyze.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_process.return_value = {"text": "test text", "cover_image_url": "test_url"}
    mock_create.return_value = {"id": 1, "title": "Test Title", "author": "Test Author"}

    result = await upload_book(db=mock_db, book_file=mock_file)
    assert result["title"] == "Test Title"

@patch("backend.main.crud.create_book")
@patch("backend.main.process_pdf")
@patch("backend.main.analyze_with_gemini")
@patch("backend.main.crud.get_book_by_path")
@pytest.mark.asyncio
async def test_upload_book_duplicate(mock_get_book, mock_analyze, mock_process, mock_create, mock_db):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = BytesIO(b"test data")
    mock_get_book.return_value = True

    with pytest.raises(HTTPException) as e:
        await upload_book(db=mock_db, book_file=mock_file)
    assert e.value.status_code == 409


@pytest.mark.asyncio
@patch("backend.main.crud.get_books")
async def test_read_books(mock_get_books, mock_db):
    mock_get_books.return_value = [{"id": 1, "title": "Book 1"}]
    result = read_books(db=mock_db)
    assert result == [{"id": 1, "title": "Book 1"}]


@patch("backend.main.crud.get_books_count")
def test_get_books_count(mock_get_books_count, mock_db):
    mock_get_books_count.return_value = 10
    result = get_books_count(db=mock_db)
    assert result == 10


@patch("backend.main.crud.get_books_by_partial_title")
def test_search_books(mock_get_books, mock_db):
    mock_get_books.return_value = [{"id": 1, "title": "Book 1"}]
    result = search_books(title="Book", db=mock_db)
    assert result == [{"id": 1, "title": "Book 1"}]


@patch("backend.main.crud.get_categories")
def test_read_categories(mock_get_categories, mock_db):
    mock_get_categories.return_value = ["Category 1"]
    result = read_categories(db=mock_db)
    assert result == ["Category 1"]


@patch("backend.main.crud.delete_book")
def test_delete_single_book(mock_delete_book, mock_db):
    mock_delete_book.return_value = {"id": 1, "title": "Book 1"}
    result = delete_single_book(book_id=1, db=mock_db)
    assert result == {"message": "Libro 'Book 1' eliminado con éxito."}


@patch("backend.main.crud.delete_books_by_category")
def test_delete_category_and_books(mock_delete_books, mock_db):
    mock_delete_books.return_value = 1
    result = delete_category_and_books(category_name="Category 1", db=mock_db)
    assert result == {"message": "Categoría 'Category 1' y sus 1 libros han sido eliminados."}



@patch("backend.main.crud.delete_book")
def test_delete_single_book_not_found(mock_delete_book, mock_db):
    mock_delete_book.return_value = None
    with pytest.raises(HTTPException) as e:
        delete_single_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404



@patch("backend.main.crud.delete_books_by_category")
def test_delete_category_and_books_not_found(mock_delete_books, mock_db):
    mock_delete_books.return_value = 0
    with pytest.raises(HTTPException) as e:
        delete_category_and_books(category_name="Category 1", db=mock_db)
    assert e.value.status_code == 404


@patch("backend.main.FileResponse")
def test_download_book(mock_fileresponse, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = {"id": 1, "file_path": "test.pdf"}
    download_book(book_id=1, db=mock_db)
    mock_fileresponse.assert_called_once()


@patch("backend.main.FileResponse")
def test_download_book_not_found(mock_fileresponse, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        download_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404


@pytest.mark.asyncio
@patch("backend.main.HTML")
@patch("backend.main.CSS")
@patch("backend.main.zipfile.ZipFile")
@patch("backend.main.tempfile.TemporaryDirectory")
async def test_convert_epub_to_pdf_success(mock_tempdir, mock_zipfile, mock_css, mock_html):
    mock_tempdir.return_value.__enter__.return_value = "test_dir"
    mock_zipfile.return_value.__enter__.return_value.extractall = MagicMock()
    mock_html.return_value.render.return_value.pages = [1]
    mock_html.return_value.render.return_value.copy.return_value.write_pdf = MagicMock()
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test data")

    result = await convert_epub_to_pdf(file=mock_file)
    assert "/temp_books/" in result["download_url"]


@pytest.mark.asyncio
@patch("backend.main.rag.process_book_for_rag")
async def test_upload_book_for_rag_success(mock_process_book, mock_db):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.read = AsyncMock(return_value=b"test data")
    mock_process_book.return_value = None

    result = await upload_book_for_rag(file=mock_file)
    assert "book_id" in result
    assert "message" in result


@pytest.mark.asyncio
@patch("backend.main.rag.process_book_for_rag")
async def test_upload_book_for_rag_error(mock_process_book):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.read = AsyncMock(return_value=b"test data")
    mock_process_book.side_effect = Exception("RAG processing error")

    with pytest.raises(HTTPException) as e:
        await upload_book_for_rag(file=mock_file)
    assert e.value.status_code == 500


@pytest.mark.asyncio
@patch("backend.main.rag.query_rag")
async def test_query_rag_endpoint_success(mock_query_rag):
    mock_query_rag.return_value = "Test response"
    query_data = {"query": "test query", "book_id": "test_id"}
    result = await query_rag_endpoint(query_data=query_data)
    assert result["response"] == "Test response"


@pytest.mark.asyncio
@patch("backend.main.rag.query_rag")
async def test_query_rag_endpoint_error(mock_query_rag):
    mock_query_rag.side_effect = Exception("RAG query error")
    query_data = {"query": "test query", "book_id": "test_id"}

    with pytest.raises(HTTPException) as e:
        await query_rag_endpoint(query_data=query_data)
    assert e.value.status_code == 500