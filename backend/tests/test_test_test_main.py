import pytest
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
import io
import os
from tempfile import NamedTemporaryFile
import json
import zipfile

# Mock de las dependencias externas

@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.all.return_value = []
    mock_db.query.return_value.filter.return_value.count.return_value = 0
    return mock_db


@pytest.fixture
def mock_crud():
    mock_crud = MagicMock()
    mock_crud.get_book_by_path.return_value = None
    mock_crud.create_book.return_value = {"id": 1, "title": "Test Book"}
    mock_crud.get_books.return_value = [{"id": 1, "title": "Test Book"}]
    mock_crud.get_books_count.return_value = 1
    mock_crud.get_books_by_partial_title.return_value = [{"id": 1, "title": "Test Book"}]
    mock_crud.get_categories.return_value = ["Category 1"]
    mock_crud.delete_book.return_value = {"id": 1, "title": "Test Book"}
    mock_crud.delete_books_by_category.return_value = 1
    return mock_crud


@pytest.fixture
def mock_rag():
    mock_rag = MagicMock()
    mock_rag.process_book_for_rag = AsyncMock()
    mock_rag.query_rag = AsyncMock(return_value="Rag response")
    return mock_rag

@patch('backend.main.genai')
@pytest.mark.asyncio
async def test_analyze_with_gemini_success(mock_genai):
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '```json\n{"title": "Test Title", "author": "Test Author", "category": "Test Category"}\n```'
    mock_genai.GenerativeModel.return_value = mock_model
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Test Title", "author": "Test Author", "category": "Test Category"}

@patch('backend.main.genai')
@pytest.mark.asyncio
async def test_analyze_with_gemini_failure(mock_genai):
    mock_genai.GenerativeModel.side_effect = Exception("Gemini API error")
    result = await analyze_with_gemini("test text")
    assert result == {"title": "Error de IA", "author": "Error de IA", "category": "Error de IA"}

@patch('backend.main.genai')
@pytest.mark.asyncio
async def test_analyze_with_gemini_empty_input(mock_genai):
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value.text = '```json\n{"title": "","author": "","category": ""}\n```'
    mock_genai.GenerativeModel.return_value = mock_model
    result = await analyze_with_gemini("")
    assert result == {"title": "", "author": "", "category": ""}

@patch('backend.main.fitz')
def test_process_pdf_success(mock_fitz):
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_page.get_text.return_value = "Test text"
    mock_doc.load_page.return_value = mock_page
    mock_doc.__len__.return_value = 5
    mock_fitz.open.return_value = mock_doc
    mock_pixmap = MagicMock()
    mock_pixmap.width = 400
    mock_pixmap.height = 400
    mock_doc.get_page_images.return_value = [(1, mock_pixmap)]
    mock_pixmap.save = MagicMock()
    result = process_pdf("test.pdf", "static/covers")
    assert "text" in result and "cover_image_url" in result

def test_process_pdf_no_cover():
    with patch('backend.main.fitz.open') as mock_open:
        mock_doc = MagicMock()
        mock_doc.get_page_images.return_value = []
        mock_open.return_value = mock_doc
        result = process_pdf("test.pdf", "static/covers")
        assert result["cover_image_url"] is None

def test_process_pdf_empty_filename():
    with pytest.raises(HTTPException) as e:
        process_pdf("", "static/covers")
    assert e.value.status_code == 400

@patch('backend.main.epub.read_epub')
def test_process_epub_success(mock_read_epub):
    mock_book = MagicMock()
    mock_item = MagicMock()
    mock_item.get_content.return_value = "<html><body>Test text</body></html>"
    mock_book.get_items_of_type.return_value = [mock_item]
    mock_read_epub.return_value = mock_book
    mock_item.get_name.return_value = "cover.jpg"
    mock_item.get_content.return_value = b"test image data"
    result = process_epub("test.epub", "static/covers")
    assert "text" in result and "cover_image_url" in result

def test_process_epub_no_text():
    with patch('backend.main.epub.read_epub') as mock_read_epub:
        mock_book = MagicMock()
        mock_book.get_items_of_type.return_value = []
        mock_read_epub.return_value = mock_book
        with pytest.raises(HTTPException):
            process_epub("test.epub", "static/covers")

def test_process_epub_empty_filename():
    with pytest.raises(HTTPException) as e:
        process_epub("", "static/covers")
    assert e.value.status_code == 400


@patch('backend.main.crud')
@patch('backend.main.shutil')
@patch('backend.main.analyze_with_gemini')
@pytest.mark.asyncio
async def test_upload_book_success(mock_analyze, mock_shutil, mock_crud, mock_db):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.file = io.BytesIO(b"test data")
    mock_analyze.return_value = {"title": "Test Title", "author": "Test Author", "category": "Test Category"}
    mock_shutil.copyfileobj = MagicMock()
    with patch('backend.main.os.path.splitext') as mock_splitext:
        mock_splitext.return_value = ("test", ".pdf")
        result = await upload_book(db=mock_db, book_file=mock_file)
        assert result["title"] == "Test Title"


@patch('backend.main.crud')
@patch('backend.main.shutil')
@patch('backend.main.analyze_with_gemini')
@pytest.mark.asyncio
async def test_upload_book_failure(mock_analyze, mock_shutil, mock_crud, mock_db):
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.file = io.BytesIO(b"test data")
    mock_analyze.return_value = {"title": "Desconocido", "author": "Desconocido", "category": "Desconocido"}
    mock_shutil.copyfileobj = MagicMock()
    with patch('backend.main.os.path.splitext') as mock_splitext:
        mock_splitext.return_value = ("test", ".pdf")
        with pytest.raises(HTTPException):
            await upload_book(db=mock_db, book_file=mock_file)

@pytest.mark.asyncio
async def test_upload_book_duplicate(mock_crud, mock_db):
    mock_crud.get_book_by_path.return_value = "Existing Book"
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.file = io.BytesIO(b"test data")
    with pytest.raises(HTTPException) as e:
        await upload_book(db=mock_db, book_file=mock_file)
    assert e.value.status_code == 409

@pytest.mark.asyncio
async def test_upload_book_empty_filename(mock_crud, mock_db):
    mock_file = MagicMock()
    mock_file.filename = ""
    mock_file.file = io.BytesIO(b"test data")
    with pytest.raises(HTTPException) as e:
        await upload_book(db=mock_db, book_file=mock_file)
    assert e.value.status_code == 400

@patch('backend.main.crud')
def test_read_books(mock_crud, mock_db):
    result = read_books(db=mock_db)
    assert result == mock_crud.get_books.return_value

def test_get_books_count(mock_crud, mock_db):
    result = get_books_count(db=mock_db)
    assert result == mock_crud.get_books_count.return_value

def test_search_books(mock_crud, mock_db):
    result = search_books(title="Test", db=mock_db)
    assert result == mock_crud.get_books_by_partial_title.return_value

def test_search_books_empty_title(mock_crud, mock_db):
    result = search_books(title="", db=mock_db)
    assert result == mock_crud.get_books_by_partial_title.return_value

def test_read_categories(mock_crud, mock_db):
    result = read_categories(db=mock_db)
    assert result == mock_crud.get_categories.return_value

@patch('backend.main.crud')
def test_delete_single_book(mock_crud, mock_db):
    mock_crud.delete_book.return_value = {"id":1, "title": "Book to delete"}
    mock_db.query.return_value.filter.return_value.first.return_value = {"id":1, "title": "Book to delete"}
    result = delete_single_book(book_id=1, db=mock_db)
    assert result == {"message": "Libro 'Book to delete' eliminado con éxito."}

    mock_crud.delete_book.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        delete_single_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404

@patch('backend.main.crud')
def test_delete_category_and_books(mock_crud, mock_db):
    result = delete_category_and_books(category_name="Test Category", db=mock_db)
    assert result == {"message": "Categoría 'Test Category' y sus 1 libros han sido eliminados."}

    mock_crud.delete_books_by_category.return_value = 0
    with pytest.raises(HTTPException) as e:
        delete_category_and_books(category_name="Test Category", db=mock_db)
    assert e.value.status_code == 404

def test_delete_category_and_books_empty_name(mock_crud, mock_db):
    with pytest.raises(HTTPException) as e:
        delete_category_and_books(category_name="", db=mock_db)
    assert e.value.status_code == 400


@patch('backend.main.crud')
def test_download_book(mock_crud, mock_db):
    mock_book = MagicMock()
    mock_book.file_path = "test.pdf"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    with patch('backend.main.FileResponse') as mock_fileresponse:
        download_book(book_id=1, db=mock_db)
        mock_fileresponse.assert_called_once()

    mock_db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as e:
        download_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404

    mock_book.file_path = "nonexistent_file.pdf"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_book
    with pytest.raises(HTTPException) as e:
        download_book(book_id=1, db=mock_db)
    assert e.value.status_code == 404

@pytest.mark.asyncio
async def test_convert_epub_to_pdf_success():
    with NamedTemporaryFile(suffix=".epub") as temp_epub:
        with zipfile.ZipFile(temp_epub, 'w') as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("META-INF/container.xml", """<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>""")
            zf.writestr("OEBPS/content.opf", """<?xml version='1.0' encoding='UTF-8'?>
            <package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookID">
                <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
                    <dc:identifier id="BookID">urn:uuid:d64a2984-773f-4404-b248-a3e93b60120a</dc:identifier>
                    <dc:title>My Epub</dc:title>
                </metadata>
                <manifest>
                    <item id="chapt1" href="Text/chapter1.html" media-type="application/xhtml+xml"/>
                </manifest>
                <spine>
                    <itemref idref="chapt1"/>
                </spine>
            </package>""")
            zf.writestr("OEBPS/Text/chapter1.html", "<html><body>Chapter 1</body></html>")

        mock_file = MagicMock()
        mock_file.filename = temp_epub.name
        mock_file.read = AsyncMock(return_value=temp_epub.read())

        result = await convert_epub_to_pdf(file=mock_file)
        assert "download_url" in result

@pytest.mark.asyncio
async def test_convert_epub_to_pdf_failure():
    mock_file = MagicMock()
    mock_file.filename = "test.txt"
    mock_file.read = AsyncMock(return_value=b"")
    with pytest.raises(HTTPException) as e:
        await convert_epub_to_pdf(file=mock_file)
    assert e.value.status_code == 400

@pytest.mark.asyncio
async def test_convert_epub_to_pdf_empty_filename():
    mock_file = MagicMock()
    mock_file.filename = ""
    mock_file.read = AsyncMock(return_value=b"")
    with pytest.raises(HTTPException) as e:
        await convert_epub_to_pdf(file=mock_file)
    assert e.value.status_code == 400


@pytest.mark.asyncio
async def test_upload_book_for_rag_success(mock_rag):
    mock_file = MagicMock()
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test data")
    result = await upload_book_for_rag(file=mock_file)
    assert "book_id" in result and "message" in result

@pytest.mark.asyncio
async def test_upload_book_for_rag_failure(mock_rag):
    mock_rag.process_book_for_rag.side_effect = Exception("RAG processing error")
    mock_file = MagicMock()
    mock_file.filename = "test.epub"
    mock_file.read = AsyncMock(return_value=b"test data")
    with pytest.raises(HTTPException) as e:
        await upload_book_for_rag(file=mock_file)
    assert e.value.status_code == 500

@pytest.mark.asyncio
async def test_upload_book_for_rag_empty_filename(mock_rag):
    mock_file = MagicMock()
    mock_file.filename = ""
    mock_file.read = AsyncMock(return_value=b"test data")
    with pytest.raises(HTTPException) as e:
        await upload_book_for_rag(file=mock_file)
    assert e.value.status_code == 400

@pytest.mark.asyncio
async def test_query_rag_endpoint_success(mock_rag):
    mock_query_data = schemas.RagQuery(query="test query", book_id="test book id")
    result = await query_rag_endpoint(query_data=mock_query_data)
    assert "response" in result

@pytest.mark.asyncio
async def test_query_rag_endpoint_failure(mock_rag):
    mock_rag.query_rag.side_effect = Exception("RAG query error")
    mock_query_data = schemas.RagQuery(query="test query", book_id="test book id")
    with pytest.raises(HTTPException) as e:
        await query_rag_endpoint(query_data=mock_query_data)
    assert e.value.status_code == 500

@pytest.mark.asyncio
async def test_query_rag_endpoint_empty_query(mock_rag):
    mock_query_data = schemas.RagQuery(query="", book_id="test book id")
    with pytest.raises(HTTPException) as e:
        await query_rag_endpoint(query_data=mock_query_data)
    assert e.value.status_code == 400

@pytest.mark.asyncio
async def test_query_rag_endpoint_empty_book_id(mock_rag):
    mock_query_data = schemas.RagQuery(query="test query", book_id="")
    with pytest.raises(HTTPException) as e:
        await query_rag_endpoint(query_data=mock_query_data)
    assert e.value.status_code == 400
```