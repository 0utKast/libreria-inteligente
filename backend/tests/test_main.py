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


@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
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
    mock_doc.get_page_images.return_value = [([1, 2, 3], 100, 100)]
    with patch('backend.main.fitz.open', return_value=mock_doc):
        result = process_pdf("test.pdf", "static/covers")
        assert result["text"] == "Test text"
        assert result["cover_image_url"] is None

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
    with pytest.raises(HTTPException) as e:
        process_epub("test.epub", "static/covers")
    assert e.value.status_code == 422

@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.crud.get_book_by_path')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.process_pdf')
@patch('backend.main.analyze_with_gemini')
async def test_upload_book_success(mock_analyze, mock_process, mock_copy, mock_get_book, mock_create):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_process.return_value = {"text": "test text", "cover_image_url": "/test.jpg"}
    mock_analyze.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_create.return_value = models.Book(id=1, title="Test Title", author="Test Author", category="Test Category", cover_image_url="/test.jpg", file_path="/test.pdf")
    mock_get_book.return_value = None
    with patch('backend.main.open', mock_open=MagicMock()) as mock_open:
        result = await upload_book(book_file=mock_file, db=MagicMock())
        mock_copy.assert_called_once()
        mock_process.assert_called_once()
        mock_analyze.assert_called_once()
        mock_create.assert_called_once()
        assert isinstance(result, models.Book)

@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.crud.get_book_by_path')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.process_pdf')
@patch('backend.main.analyze_with_gemini')
async def test_upload_book_duplicate(mock_analyze, mock_process, mock_copy, mock_get_book, mock_create):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_get_book.return_value = models.Book(id=1, title="Test Title", author="Test Author", category="Test Category", cover_image_url="/test.jpg", file_path="/test.pdf")
    with pytest.raises(HTTPException) as e:
        await upload_book(book_file=mock_file, db=MagicMock())
    assert e.value.status_code == 409

@pytest.mark.asyncio
@patch('backend.main.crud.create_book')
@patch('backend.main.crud.get_book_by_path')
@patch('backend.main.shutil.copyfileobj')
@patch('backend.main.process_pdf')
@patch('backend.main.analyze_with_gemini')
async def test_upload_book_ia_failure(mock_analyze, mock_process, mock_copy, mock_get_book, mock_create):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_process.return_value = {"text": "test text", "cover_image_url": "/test.jpg"}
    mock_analyze.return_value = {"title": "Desconocido", "author": "Desconocido", "category": "Desconocido"}
    mock_get_book.return_value = None
    with pytest.raises(HTTPException) as e:
        await upload_book(book_file=mock_file, db=MagicMock())
    assert e.value.status_code == 422

def test_read_books(mock_db):
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_book]
    result = read_books(db=mock_db)
    assert result == [mock_book]

def test_get_books_count(mock_db):
    mock_db.query.return_value.count.return_value = 10
    result = get_books_count(db=mock_db)
    assert result == 10

def test_search_books(mock_db):
    mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [mock_book]
    result = search_books(title="Test", db=mock_db)
    assert result == [mock_book]

def test_read_categories(mock_db):
    mock_db.query.return_value.distinct.return_value.all.return_value = ["Test Category"]
    result = read_categories(db=mock_db)
    assert result == ["Test Category"]

def test_delete_single_book(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    mock_db.query.return_value.filter.return_value.delete.return_value = True
    mock_db.commit.return_value = True
    result = delete_single_book(book_id=1, db=mock_db)
    assert result == {"message": "Libro 'Test Book' eliminado con éxito."}

def test_delete_single_book_not_found(mock_db):
    with pytest.raises(HTTPException) as e:
        delete_single_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404


def test_delete_category_and_books(mock_db):
    mock_db.query.return_value.filter.return_value.delete.return_value = 1
    mock_db.commit.return_value = True
    result = delete_category_and_books(category_name="Test", db=mock_db)
    assert result == {"message": "Categoría 'Test' y sus 1 libros han sido eliminados."}

def test_delete_category_and_books_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.delete.return_value = 0
    with pytest.raises(HTTPException) as e:
        delete_category_and_books(category_name="Test", db=mock_db)
    assert e.value.status_code == 404

def test_download_book(mock_db, mock_book):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    with patch('backend.main.FileResponse') as mock_fileresp:
        download_book(book_id=1, db=mock_db)
        mock_fileresp.assert_called_once()

def test_download_book_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        download_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404

@pytest.mark.asyncio
@patch('backend.main.HTML')
@patch('backend.main.CSS')
@patch('backend.main.BeautifulSoup')
@patch('backend.main.zipfile.ZipFile')
@patch('backend.main.tempfile.TemporaryDirectory')
async def test_convert_epub_to_pdf_success(mock_tempdir, mock_zipfile, mock_bs4, mock_css, mock_html):
    mock_file = MagicMock()
    mock_file.filename = "test.epub"
    mock_file.read.return_value = b"test epub content"
    mock_tempdir.return_value = "test_temp_dir"
    mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None
    mock_bs4.return_value.find.return_value = {"content": "test_id", 'href': 'test.xhtml'}
    mock_bs4.return_value.find_all.side_effect = lambda *args, **kwargs: []
    mock_html.return_value.render.return_value.pages = [MagicMock()]
    mock_html.return_value.render.return_value.copy.return_value.write_pdf.return_value = None

    mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None

    with patch('backend.main.open', mock_open=MagicMock()) as mock_open:
        with patch('backend.main.uuid.uuid4', return_value=uuid.UUID("00000000-0000-0000-0000-000000000000")):
          result = await convert_epub_to_pdf(file=mock_file)
          assert result["download_url"] == "/temp_books/00000000-0000-0000-0000-000000000000.pdf"

@pytest.mark.asyncio
async def test_convert_epub_to_pdf_failure():
    mock_file = MagicMock()
    mock_file.filename = "test.epub"
    mock_file.read.return_value = b"test epub content"
    with pytest.raises(HTTPException) as e:
        await convert_epub_to_pdf(file=mock_file)  #Simula una excepción en la conversion
    assert e.value.status_code == 500


@pytest.mark.asyncio
@patch('backend.main.rag.process_book_for_rag')
async def test_upload_book_for_rag_success(mock_process_book):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.read.return_value = b"test content"
    with patch('backend.main.open', mock_open=MagicMock()):
        result = await upload_book_for_rag(file=mock_file)
        mock_process_book.assert_called_once()
        assert result["message"] == "Libro procesado para RAG exitosamente."

@pytest.mark.asyncio
@patch('backend.main.rag.process_book_for_rag')
async def test_upload_book_for_rag_failure(mock_process_book):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.read.return_value = b"test content"
    mock_process_book.side_effect = Exception("RAG processing error")
    with pytest.raises(HTTPException) as e:
        await upload_book_for_rag(file=mock_file)
    assert e.value.status_code == 500

@pytest.mark.asyncio
@patch('backend.main.rag.query_rag')
async def test_query_rag_endpoint_success(mock_query_rag):
    mock_query_data = schemas.RagQuery(query="test query", book_id="test_book_id")
    mock_query_rag.return_value = "test response"
    result = await query_rag_endpoint(query_data=mock_query_data)
    assert result["response"] == "test response"

@pytest.mark.asyncio
@patch('backend.main.rag.query_rag')
async def test_query_rag_endpoint_failure(mock_query_rag):
    mock_query_data = schemas.RagQuery(query="test query", book_id="test_book_id")
    mock_query_rag.side_effect = Exception("RAG query error")
    with pytest.raises(HTTPException) as e:
        await query_rag_endpoint(query_data=mock_query_data)
    assert e.value.status_code == 500
