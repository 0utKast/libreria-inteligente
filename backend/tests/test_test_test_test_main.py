import pytest
import uuid
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
import ebooklib
import os

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.all.return_value = []
    mock_db.query.return_value.count.return_value = 0
    mock_db.query.return_value.distinct.return_value.all.return_value = []
    mock_db.commit.return_value = True
    mock_db.add.return_value = None
    mock_db.delete.return_value = None
    mock_db.rollback.return_value = None
    return mock_db


@pytest.fixture
def mock_book():
    return models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="/test.jpg", file_path="/test.pdf")

@pytest.fixture
def mock_book_data():
    return {"title": "Test Book", "author": "Test Author", "category": "Test Category", "text": "Test text", "cover_image_url": "/test.jpg", "file_path": "/test.pdf"}


@pytest.mark.asyncio
async def test_analyze_with_gemini_success():
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '{"title": "Test Title", "author": "Test Author", "category": "Test Category"}'
    with patch('backend.main.genai.GenerativeModel', return_value=mock_model):
        result = await analyze_with_gemini("test text")
        assert result == {"title": "Test Title", "author": "Test Author", "category": "Test Category"}

@pytest.mark.asyncio
async def test_analyze_with_gemini_failure():
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("Gemini API error")
    with patch('backend.main.genai.GenerativeModel', return_value=mock_model):
        result = await analyze_with_gemini("test text")
        assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}

@pytest.mark.asyncio
async def test_analyze_with_gemini_empty_text():
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '{"title": "Test Title", "author": "Test Author", "category": "Test Category"}'
    with patch('backend.main.genai.GenerativeModel', return_value=mock_model):
        result = await analyze_with_gemini("")
        assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}

@patch('backend.main.fitz.open')
def test_process_pdf_success(mock_fitz_open):
    mock_doc = MagicMock()
    mock_doc.load_page.return_value.get_text.return_value = "Test text"
    mock_fitz_open.return_value = mock_doc
    mock_doc.get_page_images.return_value = [([1, 2, 3], 100, 100), ([4, 5, 6], 400, 400)]
    with patch('backend.main.os.path.join', return_value = "test_path"):
      with patch('backend.main.fitz.Pixmap.save') as mock_save:
        result = process_pdf("test.pdf", "static/covers")
        mock_save.assert_called_once()
        assert result["text"] == "Test text"
        assert result["cover_image_url"] == "static/covers/cover_test.pdf.png"

def test_process_pdf_no_cover():
    mock_doc = MagicMock()
    mock_doc.load_page.return_value.get_text.return_value = "Test text"
    mock_doc.get_page_images.return_value = []
    with patch('backend.main.fitz.open', return_value=mock_doc):
        result = process_pdf("test.pdf", "static/covers")
        assert result["text"] == "Test text"
        assert result["cover_image_url"] is None

def test_process_pdf_empty_text():
    mock_doc = MagicMock()
    mock_doc.load_page.return_value.get_text.return_value = ""
    mock_doc.get_page_images.return_value = []
    with patch('backend.main.fitz.open', return_value=mock_doc):
        with pytest.raises(HTTPException) as e:
            process_pdf("test.pdf", "static/covers")
        assert e.value.status_code == 422

@patch('backend.main.epub.read_epub')
def test_process_epub_success(mock_read_epub):
    mock_book = MagicMock()
    mock_book.get_items_of_type.return_value = [{'get_content': lambda: '<html><body>Test text</body></html>', 'get_name': lambda: 'cover.jpg'}]
    mock_read_epub.return_value = mock_book
    with patch('backend.main.open', mock_open=MagicMock()):
        result = process_epub("test.epub", "static/covers")
        assert "Test text" in result["text"]
        assert result["cover_image_url"] == "static/covers/cover_test.epub_cover.jpg"

@patch('backend.main.epub.read_epub')
def test_process_epub_no_cover(mock_read_epub):
    mock_book = MagicMock()
    mock_book.get_items_of_type.side_effect = lambda x: [] if x == ebooklib.ITEM_COVER else [{'get_content': lambda: '<html><body>Test text</body></html>'}]
    mock_read_epub.return_value = mock_book
    with patch('backend.main.open', mock_open=MagicMock()):
        result = process_epub("test.epub", "static/covers")
        assert "Test text" in result["text"]
        assert result["cover_image_url"] is None

@patch('backend.main.epub.read_epub')
def test_process_epub_insufficient_text(mock_read_epub):
    mock_book = MagicMock()
    mock_book.get_items_of_type.return_value = [{'get_content': lambda: '<html><body>Short text</body></html>'}]
    mock_read_epub.return_value = mock_book
    with patch('backend.main.open', mock_open=MagicMock()):
        with pytest.raises(HTTPException) as e:
            process_epub("test.epub", "static/covers")
        assert e.value.status_code == 422

@pytest.mark.asyncio
async def test_upload_book_success(mock_db, mock_book_data):
    with patch('backend.main.process_pdf', return_value=mock_book_data), patch('backend.main.analyze_with_gemini', return_value=mock_book_data):
        file = BytesIO(b"test file")
        file.name = "test.pdf"
        result = await upload_book(file, mock_db)
        mock_db.add.assert_called_once()
        assert result.title == "Test Book"

@pytest.mark.asyncio
async def test_upload_book_failure(mock_db):
    file = BytesIO(b"test file")
    file.name = "test.pdf"
    with patch('backend.main.process_pdf', side_effect=Exception("Error processing PDF")):
        with pytest.raises(HTTPException) as e:
            await upload_book(file, mock_db)
        assert e.value.status_code == 422

@pytest.mark.asyncio
async def test_read_books(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_book]
    books = await read_books(mock_db)
    assert len(books) == 1
    assert books[0].title == "Test Book"

@pytest.mark.asyncio
async def test_get_books_count(mock_db):
    mock_db.query.return_value.count.return_value = 5
    count = await get_books_count(mock_db)
    assert count == 5

@pytest.mark.asyncio
async def test_search_books(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_book]
    books = await search_books("Test", mock_db)
    assert len(books) == 1
    assert books[0].title == "Test Book"


@pytest.mark.asyncio
async def test_read_categories(mock_db):
    mock_db.query.return_value.distinct.return_value.all.return_value = ["Category 1", "Category 2"]
    categories = await read_categories(mock_db)
    assert len(categories) == 2
    assert "Category 1" in categories
    assert "Category 2" in categories

@pytest.mark.asyncio
async def test_delete_single_book(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    await delete_single_book(1, mock_db)
    mock_db.delete.assert_called_once_with(mock_book)
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_delete_single_book_not_found(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        await delete_single_book(1, mock_db)
    assert e.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_category_and_books(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_book]
    await delete_category_and_books("Test Category", mock_db)
    mock_db.delete.assert_called()
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_download_book(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    with patch('backend.main.open', mock_open=MagicMock(return_value=BytesIO(b"test file"))):
        with patch('backend.main.os.path.exists', return_value=True):
            file = await download_book(1, mock_db)
            assert file.read() == b"test file"

@pytest.mark.asyncio
async def test_download_book_not_found(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        await download_book(1, mock_db)
    assert e.value.status_code == 404

@pytest.mark.asyncio
async def test_convert_epub_to_pdf(mock_db, mock_book):
    with patch('backend.main.subprocess.run') as mock_subprocess:
        await convert_epub_to_pdf("test.epub", "test.pdf")
        mock_subprocess.assert_called_once()


@pytest.mark.asyncio
async def test_upload_book_for_rag(mock_db, mock_book_data):
    with patch('backend.main.process_pdf', return_value=mock_book_data), patch('backend.main.analyze_with_gemini', return_value=mock_book_data), patch('backend.main.query_rag_endpoint') as mock_rag:
        file = BytesIO(b"test file")
        file.name = "test.pdf"
        await upload_book_for_rag(file, mock_db)
        mock_rag.assert_called_once()


@pytest.mark.asyncio
async def test_query_rag_endpoint():
    with patch('backend.main.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response
        result = await query_rag_endpoint({"text": "test"})
        assert result == {"result": "success"}

@pytest.mark.asyncio
async def test_query_rag_endpoint_failure():
    with patch('backend.main.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        with pytest.raises(HTTPException) as e:
            await query_rag_endpoint({"text": "test"})
        assert e.value.status_code == 500

@pytest.mark.asyncio
async def test_query_rag_endpoint_exception():
    with patch('backend.main.requests.post') as mock_post:
        mock_post.side_effect = Exception("Network Error")
        with pytest.raises(HTTPException) as e:
            await query_rag_endpoint({"text": "test"})
        assert e.value.status_code == 500
