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

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.all.return_value = []
    mock_db.query.return_value.count.return_value = 0
    mock_db.query.return_value.distinct.return_value.all.return_value = []
    mock_db.commit.return_value = True
    return mock_db


@pytest.fixture
def mock_book():
    return models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="/test.jpg", file_path="/test.pdf")

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

# ... (rest of the test functions remain largely the same)
