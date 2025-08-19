import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile, HTTPException
from backend.main import (
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
from backend.crud import crud
from backend.models import Book
from backend import schemas
import io
import os
import uuid

#Mocks
mock_db = MagicMock()
mock_crud = MagicMock()
mock_rag = MagicMock()

@patch('backend.main.genai')
async def test_analyze_with_gemini_success(mock_genai):
    mock_model = AsyncMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = AsyncMock()
    mock_response.text = "```json\n{'title': 'Test Title', 'author': 'Test Author', 'category': 'Test Category'}\n```"
    mock_model.generate_content_async.return_value = mock_response
    result = await analyze_with_gemini("test text")
    assert result == {'title': 'Test Title', 'author': 'Test Author', 'category': 'Test Category'}

@patch('backend.main.genai')
async def test_analyze_with_gemini_error(mock_genai):
    mock_genai.GenerativeModel.side_effect = Exception("Gemini API Error")
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}

@patch('backend.main.fitz')
def test_process_pdf_success(mock_fitz):
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "test text"
    mock_doc.load_page.return_value = mock_page
    mock_doc.__len__.return_value = 5
    mock_fitz.open.return_value = mock_doc
    mock_pix = MagicMock()
    mock_pix.width = 400
    mock_pix.height = 400
    mock_doc.get_page_images.return_value = [(1,mock_pix)]
    mock_pix.save = MagicMock()

    result = process_pdf("test.pdf", "static/covers")
    assert "text" in result
    assert "cover_image_url" in result

def test_process_pdf_no_cover():
    mock_fitz = MagicMock()
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 5
    mock_page = MagicMock()
    mock_page.get_text.return_value = "Test Text"
    mock_doc.load_page.return_value = mock_page
    mock_doc.get_page_images.return_value = []
    mock_fitz.open.return_value = mock_doc
    result = process_pdf("test.pdf", "static/covers")
    assert result["cover_image_url"] is None

def test_process_epub_success():
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body>Test EPUB content</body></html>"
    mock_book.get_items_of_type.side_effect = lambda x: [mock_item] if x == ebooklib.ITEM_DOCUMENT else [MagicMock()]
    mock_item.get_name.return_value = "cover.jpg"
    mock_item.get_content.return_value = b"test_content"

    with patch('backend.main.epub.read_epub', return_value=mock_book):
        with patch('backend.main.open', mock_open=MagicMock()):
            result = process_epub("test.epub", "static/covers")
            assert "text" in result
            assert "cover_image_url" in result

def test_process_epub_no_cover():
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body>Test EPUB content</body></html>"
    mock_book.get_items_of_type.side_effect = lambda x: [mock_item] if x == ebooklib.ITEM_DOCUMENT else []
    with patch('backend.main.epub.read_epub', return_value=mock_book):
        result = process_epub("test.epub", "static/covers")
        assert "text" in result
        assert "cover_image_url" is None

@patch('backend.main.crud.create_book')
@patch('backend.main.process_pdf')
@patch('backend.main.analyze_with_gemini', new_callable=AsyncMock)
async def test_upload_book_pdf(mock_analyze, mock_process, mock_create):
    mock_file = MagicMock(spec=UploadFile, filename="test.pdf", file=io.BytesIO(b"test"))
    mock_analyze.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_process.return_value = {"text": "Test text", "cover_image_url": "Test cover URL"}
    mock_create.return_value = {"id": 1, "title": "Test Title", "author": "Test Author", "category": "Test Category", "cover_image_url": "Test cover URL", "file_path": "books/test.pdf"}
    mock_crud.get_book_by_path.return_value = None
    result = await upload_book(db=mock_db, book_file=mock_file)
    assert result == {"id": 1, "title": "Test Title", "author": "Test Author", "category": "Test Category", "cover_image_url": "Test cover URL", "file_path": "books/test.pdf"}
    mock_create.assert_called_once()


@patch('backend.main.crud.create_book')
@patch('backend.main.process_epub')
@patch('backend.main.analyze_with_gemini', new_callable=AsyncMock)
async def test_upload_book_epub(mock_analyze, mock_process, mock_create):
    mock_file = MagicMock(spec=UploadFile, filename="test.epub", file=io.BytesIO(b"test"))
    mock_analyze.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_process.return_value = {"text": "Test text", "cover_image_url": "Test cover URL"}
    mock_create.return_value = {"id": 1, "title": "Test Title", "author": "Test Author", "category": "Test Category", "cover_image_url": "Test cover URL", "file_path": "books/test.epub"}
    mock_crud.get_book_by_path.return_value = None

    result = await upload_book(db=mock_db, book_file=mock_file)
    assert result == {"id": 1, "title": "Test Title", "author": "Test Author", "category": "Test Category", "cover_image_url": "Test cover URL", "file_path": "books/test.epub"}
    mock_create.assert_called_once()

@patch('backend.main.crud.get_books')
def test_read_books(mock_get_books):
    mock_get_books.return_value = [{"id": 1, "title": "Book 1"}]
    result = read_books(db=mock_db)
    assert result == [{"id": 1, "title": "Book 1"}]

@patch('backend.main.crud.get_books_count')
def test_get_books_count(mock_get_books_count):
    mock_get_books_count.return_value = 10
    result = get_books_count(db=mock_db)
    assert result == 10

@patch('backend.main.crud.get_books_by_partial_title')
def test_search_books(mock_search_books):
    mock_search_books.return_value = [{"id": 1, "title": "Book 1"}]
    result = search_books(title="Book", db=mock_db)
    assert result == [{"id": 1, "title": "Book 1"}]

@patch('backend.main.crud.get_categories')
def test_read_categories(mock_get_categories):
    mock_get_categories.return_value = ["Category 1", "Category 2"]
    result = read_categories(db=mock_db)
    assert result == ["Category 1", "Category 2"]

@patch('backend.main.crud.delete_book')
def test_delete_single_book(mock_delete_book):
    mock_delete_book.return_value = Book(id=1, title="Book 1")
    result = delete_single_book(book_id=1, db=mock_db)
    assert result == {"message": "Libro 'Book 1' eliminado con éxito."}

@patch('backend.main.crud.delete_books_by_category')
def test_delete_category_and_books(mock_delete_books):
    mock_delete_books.return_value = 1
    result = delete_category_and_books(category_name="Category 1", db=mock_db)
    assert result == {"message": "Categoría 'Category 1' y sus 1 libros han sido eliminados."}

@patch('backend.main.crud.get_book_by_id')
def test_download_book(mock_get_book):
    mock_book = Book(id=1, file_path="test.pdf")
    mock_get_book.return_value = mock_book
    result = download_book(book_id=1, db=mock_db)
    assert result is not None

@patch('backend.main.uuid.uuid4', return_value=uuid.UUID('f47ac10b-58cc-4372-a567-0e02b2c3d479'))
@patch('backend.main.open', new_callable=MagicMock)
@patch('backend.main.HTML')
async def test_convert_epub_to_pdf(mock_html,mock_open,mock_uuid):
    mock_file = MagicMock(spec=UploadFile, filename="test.epub", file=io.BytesIO(b"test"))
    mock_html.return_value.render.return_value.pages = []
    mock_html.return_value.render.return_value.copy.return_value.write_pdf = MagicMock()

    result = await convert_epub_to_pdf(file=mock_file)
    assert result["download_url"] == "/temp_books/f47ac10b-58cc-4372-a567-0e02b2c3d479.pdf"


@patch('backend.main.rag.process_book_for_rag', new_callable=AsyncMock)
async def test_upload_book_for_rag(mock_process_book):
    mock_file = MagicMock(spec=UploadFile, filename="test.epub", file=io.BytesIO(b"test"))
    result = await upload_book_for_rag(file=mock_file)
    assert result["book_id"] == str(uuid.uuid4())
    assert result["message"] == "Libro procesado para RAG exitosamente."
    mock_process_book.assert_called_once()

@patch('backend.main.rag.query_rag', new_callable=AsyncMock)
async def test_query_rag_endpoint(mock_query_rag):
    mock_query_data = schemas.RagQuery(query="test query", book_id="test book id")
    mock_query_rag.return_value = "test response"
    result = await query_rag_endpoint(query_data=mock_query_data)
    assert result["response"] == "test response"
    mock_query_rag.assert_called_once()
