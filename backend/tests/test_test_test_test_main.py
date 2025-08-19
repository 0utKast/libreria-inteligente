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
from unittest.mock import mock_open
import fitz  # Assuming fitz is used for PDF processing


@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
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
    mock_doc.get_page_images.return_value = [MagicMock(x0=0, y0=0, x1=100, y1=100, name="cover.jpg")]
    mock_fitz_open.return_value = mock_doc
    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        file_path = temp_file.name
    with patch('backend.main.shutil.copy') as mock_shutil_copy:
        result = process_pdf(file_path, "static/covers")
        mock_shutil_copy.assert_called_once()
    os.remove(file_path)
    assert "text" in result
    assert result["text"].startswith("This is a test PDF.")
    assert result["cover_image_url"] == "static/covers/cover.jpg"


def test_process_pdf_no_cover():
    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        file_path = temp_file.name
    with patch("backend.main.fitz.open") as mock_open:
        mock_doc = MagicMock()
        mock_doc.get_page_images.return_value = []
        mock_open.return_value = mock_doc
        result = process_pdf(file_path, "static/covers")
    os.remove(file_path)
    assert "text" in result
    assert result["cover_image_url"] is None

def test_process_pdf_empty_file():
    with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        file_path = temp_file.name
    with patch("backend.main.fitz.open") as mock_open:
        mock_open.side_effect = fitz.fitz.EmptyFileError("Empty PDF file")
        with pytest.raises(Exception) as excinfo:
            process_pdf(file_path, "static/covers")
        assert "Empty PDF file" in str(excinfo.value)
    os.remove(file_path)


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
    mock_create_book.return_value = models.Book(id=1, title="Test Title", author="Test Author", category="Test Category", cover_image_url="test.jpg", file_path="test.pdf")

    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = io.BytesIO(b"test")

    with patch('backend.main.database.SessionLocal') as mock_session:
        result = upload_book(db=mock_session.return_value, book_file=mock_file)
    assert result["title"] == "Test Title"

# ... (rest of the tests remain largely the same, but you might need to adjust mocks for specific functions  like  crud functions to return appropriate mock objects.  Also ensure that all functions that interact with the database are properly mocked and that commit and refresh methods on the mock db are called where appropriate.  Consider adding tests for various failure scenarios  in each function.)
