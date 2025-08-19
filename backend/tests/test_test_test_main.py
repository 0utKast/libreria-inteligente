import pytest
import os
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
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
    return mock_db

@pytest.fixture
def mock_book():
    return models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="/path/to/cover", file_path="/path/to/file")

@pytest.fixture
def mock_file():
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.file = BytesIO(b"test")
    return mock_file

@pytest.fixture
def mock_file_epub():
    mock_file = MagicMock()
    mock_file.filename = "test.epub"
    mock_file.read.return_value = b"test epub content"
    return mock_file

@pytest.mark.asyncio
async def test_analyze_with_gemini_success():
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '```json\n{"title": "Test Title", "author": "Test Author", "category": "Test Category"}\n```'
    with patch('backend.main.genai.GenerativeModel', return_value=mock_model):
        result = await analyze_with_gemini("test text")
        assert result == {"title": "Test Title", "author": "Test Author", "category": "Test Category"}

@pytest.mark.asyncio
async def test_analyze_with_gemini_failure():
    mock_model = AsyncMock()
    mock_model.generate_content_async.side_effect = Exception("Gemini API Error")
    with patch('backend.main.genai.GenerativeModel', return_value=mock_model):
        result = await analyze_with_gemini("test text")
        assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}

@pytest.mark.asyncio
async def test_analyze_with_gemini_empty_input():
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '```json\n{"title": "Test Title", "author": "Test Author", "category": "Test Category"}\n```'
    with patch('backend.main.genai.GenerativeModel', return_value=mock_model):
        result = await analyze_with_gemini("")
        assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}


@patch('backend.main.fitz.open')
def test_process_pdf_success(mock_fitz_open):
    mock_doc = MagicMock()
    mock_doc.load_page.return_value.get_text.return_value = "Test Text"
    mock_fitz_open.return_value = mock_doc
    mock_pixmap = MagicMock()
    mock_pixmap.width = 400
    mock_pixmap.height = 400
    mock_doc.get_page_images.return_value = [[1, mock_pixmap]]
    mock_pixmap.save = MagicMock()
    result = process_pdf("test.pdf", "static/covers")
    assert "Test Text" in result["text"]
    assert "cover_test.pdf.png" in result["cover_image_url"]

def test_process_pdf_no_cover():
    mock_doc = MagicMock()
    mock_doc.load_page.return_value.get_text.return_value = "Test Text"
    mock_doc.get_page_images.return_value = []
    with patch('backend.main.fitz.open', return_value=mock_doc):
        result = process_pdf("test.pdf", "static/covers")
        assert "Test Text" in result["text"]
        assert result["cover_image_url"] is None

def test_process_pdf_empty_file():
    with patch('backend.main.fitz.open', side_effect=Exception("Error opening file")):
        with pytest.raises(Exception) as e:
            process_pdf("", "static/covers")
        assert "Error opening file" in str(e.value)

@patch('backend.main.epub.read_epub')
def test_process_epub_success(mock_read_epub):
    mock_book = MagicMock()
    mock_book.get_items_of_type.return_value = [MagicMock(get_content=lambda: "<p>Test Text</p>", get_name=lambda: "cover.jpg")]
    mock_read_epub.return_value = mock_book
    with patch('backend.main.open', mock_open=MagicMock()):
        result = process_epub("test.epub", "static/covers")
        assert "Test Text" in result["text"]
        assert "cover_test.epub_cover.jpg" in result["cover_image_url"]

def test_process_epub_no_cover():
    mock_book = MagicMock()
    mock_book.get_items_of_type.side_effect = lambda x: [] if x == ebooklib.ITEM_COVER else [MagicMock(get_content=lambda: "<p>Test Text</p>")]
    with patch('backend.main.epub.read_epub', return_value=mock_book):
        result = process_epub("test.epub", "static/covers")
        assert "Test Text" in result["text"]
        assert result["cover_image_url"] is None

def test_process_epub_empty_file():
    with patch('backend.main.epub.read_epub', side_effect=Exception("Error reading epub")):
        with pytest.raises(Exception) as e:
            process_epub("", "static/covers")
        assert "Error reading epub" in str(e.value)


@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.crud.get_book_by_path')
async def test_upload_book_success(mock_get_book, mock_copy, mock_create_book, mock_file, mock_db):
    mock_get_book.return_value = None
    mock_create_book.return_value = models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="/path/to/cover", file_path="/path/to/file")
    with patch('backend.main.process_pdf', return_value={"text": "test", "cover_image_url": "/path/to/cover"}):
        with patch('backend.main.analyze_with_gemini', return_value={"title": "Test Title", "author": "Test Author", "category": "Test Category"}):
            result = await upload_book(db=mock_db, book_file=mock_file)
            assert result.title == "Test Book"
            mock_create_book.assert_called_once()

@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.crud.get_book_by_path')
async def test_upload_book_already_exists(mock_get_book, mock_copy, mock_create_book, mock_file, mock_db):
    mock_get_book.return_value = models.Book(id=1, title="Test Book", author="Test Author", category="Test Category", cover_image_url="/path/to/cover", file_path="/path/to/file")
    with pytest.raises(HTTPException) as e:
        await upload_book(db=mock_db, book_file=mock_file)
    assert e.value.status_code == 409

@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.crud.get_book_by_path')
async def test_upload_book_ia_failure(mock_get_book, mock_copy, mock_create_book, mock_file, mock_db):
    mock_get_book.return_value = None
    with patch('backend.main.process_pdf', return_value={"text": "test", "cover_image_url": "/path/to/cover"}):
        with patch('backend.main.analyze_with_gemini', return_value={"title": "Desconocido", "author": "Desconocido", "category": "Desconocido"}):
            with pytest.raises(HTTPException) as e:
                await upload_book(db=mock_db, book_file=mock_file)
            assert e.value.status_code == 422

@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.crud.get_book_by_path')
async def test_upload_book_process_pdf_failure(mock_get_book, mock_copy, mock_create_book, mock_file, mock_db):
    mock_get_book.return_value = None
    with patch('backend.main.process_pdf', side_effect=Exception("PDF processing error")):
        with pytest.raises(Exception) as e:
            await upload_book(db=mock_db, book_file=mock_file)
        assert "PDF processing error" in str(e.value)


def test_read_books(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_book]
    mock_crud_get_books = MagicMock(return_value=[mock_book])
    with patch('backend.main.crud.get_books', mock_crud_get_books):
        books = read_books(db=mock_db)
        assert len(books) == 1

def test_get_books_count(mock_db):
    mock_db.query.return_value.count.return_value = 10
    mock_crud_get_books_count = MagicMock(return_value=10)
    with patch('backend.main.crud.get_books_count', mock_crud_get_books_count):
        count = get_books_count(db=mock_db)
        assert count == 10

def test_search_books(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_book]
    mock_crud_get_books_by_partial_title = MagicMock(return_value=[mock_book])
    with patch('backend.main.crud.get_books_by_partial_title', mock_crud_get_books_by_partial_title):
        books = search_books(title="Test", db=mock_db)
        assert len(books) == 1

def test_read_categories(mock_db):
    mock_db.query.return_value.distinct.return_value.all.return_value = ["Test Category"]
    mock_crud_get_categories = MagicMock(return_value=["Test Category"])
    with patch('backend.main.crud.get_categories', mock_crud_get_categories):
        categories = read_categories(db=mock_db)
        assert categories == ["Test Category"]

def test_delete_single_book(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    mock_crud_delete_book = MagicMock(return_value=mock_book)
    with patch('backend.main.crud.delete_book', mock_crud_delete_book):
        result = delete_single_book(book_id=1, db=mock_db)
        assert result == {"message": f"Libro '{mock_book.title}' eliminado con éxito."}

def test_delete_single_book_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_crud_delete_book = MagicMock(return_value=None)
    with patch('backend.main.crud.delete_book', mock_crud_delete_book):
        with pytest.raises(HTTPException) as e:
            delete_single_book(book_id=1, db=mock_db)
        assert e.value.status_code == 404

def test_delete_category_and_books(mock_db):
    mock_crud_delete_books_by_category = MagicMock(return_value=1)
    with patch('backend.main.crud.delete_books_by_category', mock_crud_delete_books_by_category):
        result = delete_category_and_books(category_name="Test Category", db=mock_db)
        assert result == {"message": "Categoría 'Test Category' y sus 1 libros han sido eliminados."}

def test_delete_category_and_books_not_found(mock_db):
    mock_crud_delete_books_by_category = MagicMock(return_value=0)
    with patch('backend.main.crud.delete_books_by_category', mock_crud_delete_books_by_category):
        with pytest.raises(HTTPException) as e:
            delete_category_and_books(category_name="Test Category", db=mock_db)
        assert e.value.status_code == 404

def test_download_book(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    mock_file_response = MagicMock()
    with patch('backend.main.FileResponse', return_value=mock_file_response):
        response = download_book(book_id=1, db=mock_db)
        assert response == mock_file_response

def test_download_book_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        download_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404

@pytest.mark.asyncio
@patch('backend.main.uuid.uuid4', return_value=MagicMock(hex='test_uuid'))
async def test_convert_epub_to_pdf_success(mock_uuid4, mock_file_epub):
    with patch('backend.main.HTML.render', return_value=MagicMock(pages=[], copy=lambda x: MagicMock(write_pdf=MagicMock()))):
        with patch('backend.main.open', mock_open=MagicMock()):
            response = await convert_epub_to_pdf(file=mock_file_epub)
            assert response["download_url"] == "/temp_books/test_uuid.pdf"

@pytest.mark.asyncio
async def test_convert_epub_to_pdf_invalid_file():
    mock_file = MagicMock()
    mock_file.filename = "test.txt"
    with pytest.raises(HTTPException) as e:
        await convert_epub_to_pdf(file=mock_file)
    assert e.value.status_code == 400

@pytest.mark.asyncio
@patch('backend.main.uuid.uuid4', return_value=MagicMock(hex='test_uuid'))
@patch('backend.main.rag.process_book_for_rag')
async def test_upload_book_for_rag_success(mock_process_book, mock_file, mock_file_epub):
    mock_file_epub.filename = "test.epub"
    mock_file_epub.read.return_value = b"test content"
    with patch('backend.main.open', mock_open=MagicMock()):
        response = await upload_book_for_rag(file=mock_file_epub)
        assert response["book_id"] == "test_uuid"
        mock_process_book.assert_called_once()

@pytest.mark.asyncio
@patch('backend.main.rag.process_book_for_rag')
async def test_upload_book_for_rag_failure(mock_process_book, mock_file_epub):
    mock_process_book.side_effect = Exception("RAG processing error")
    mock_file_epub.filename = "test.pdf"
    mock_file_epub.read.return_value = b"test content"
    with patch('backend.main.uuid.uuid4', return_value=MagicMock(hex='test_uuid')):
        with pytest.raises(HTTPException) as e:
            await upload_book_for_rag(file=mock_file_epub)
        assert e.value.status_code == 500

@pytest.mark.asyncio
@patch('backend.main.rag.query_rag')
async def test_query_rag_endpoint_success(mock_query_rag):
    mock_query_rag.return_value = "Test RAG response"
    response = await query_rag_endpoint(query_data=schemas.RagQuery(query="test query", book_id="test_book_id"))
    assert response["response"] == "Test RAG response"

@pytest.mark.asyncio
@patch('backend.main.rag.query_rag')
async def test_query_rag_endpoint_failure(mock_query_rag):
    mock_query_rag.side_effect = Exception("RAG query error")
    with pytest.raises(HTTPException) as e:
        await query_rag_endpoint(query_data=schemas.RagQuery(query="test query", book_id="test_book_id"))
    assert e.value.status_code == 500