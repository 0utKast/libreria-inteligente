# DOCUMENTACION_PROYECTO.md

## 1. Descripción General del Proyecto

"Mi Librería Inteligente" es una aplicación web que permite a los usuarios gestionar y organizar su colección de libros digitales.  La aplicación ofrece funcionalidades para subir libros (PDF y EPUB), buscar libros por título, autor o categoría,  convertir EPUB a PDF,  y consultar un sistema de Recuperación de la Información basada en preguntas y respuestas (RAG) sobre el contenido de los libros.

La arquitectura de la aplicación se basa en un frontend desarrollado con React.js, un backend construido con FastAPI (Python) y una base de datos SQLite.  El sistema RAG utiliza la API de Google Generative AI para generar embeddings y responder preguntas.


## 2. Estructura del Proyecto

El proyecto se divide en dos partes principales: el backend (Python) y el frontend (React).

*   **backend/**: Contiene el código del backend de FastAPI.
    *   **schemas.py**: Define los modelos Pydantic para la serialización y validación de datos.
    *   **crud.py**: Contiene la lógica de acceso a datos (CRUD) para la base de datos.
    *   **database.py**: Configura la conexión a la base de datos SQLite.
    *   **models.py**: Define el modelo de datos SQLAlchemy para la tabla `books`.
    *   **rag.py**: Implementa la lógica del sistema RAG (Recuperación de la Información basada en preguntas y respuestas).
    *   **main.py**: Define las rutas de la API FastAPI.
    *   **alembic/**: Contiene los scripts de migración de la base de datos.
    *   **tests/**: Contiene las pruebas unitarias del backend.

*   **frontend/src/**: Contiene el código del frontend de React.
    *   **App.js**: Componente principal de la aplicación React.
    *   **Header.js**: Componente de encabezado de la aplicación.
    *   **LibraryView.js**: Componente que muestra la lista de libros.
    *   **UploadView.js**: Componente para subir libros.
    *   **CategoriesView.js**: Componente que muestra la lista de categorías.
    *   **ToolsView.js**: Componente que contiene herramientas adicionales.
    *   **ReaderView.js**: Componente para la lectura de libros EPUB.
    *   **RagView.js**: Componente para la interacción con el sistema RAG.
    *   **config.js**: Configura la URL base de la API.


## 3. Análisis Detallado del Backend (Python/FastAPI)

### backend/schemas.py

Este archivo define los modelos Pydantic usados para la serialización y validación de datos en la API.

*   **Clase `BookBase`**: Modelo base para un libro.
    *   `title: str`: Título del libro (requerido).
    *   `author: str`: Autor del libro (requerido).
    *   `category: str`: Categoría del libro (requerido).
    *   `cover_image_url: str | None = None`: URL de la imagen de portada (opcional).
    *   `file_path: str`: Ruta al archivo del libro (requerido).

*   **Clase `Book`**: Modelo para un libro, extiende `BookBase`.
    *   `id: int`: ID del libro (autoincremental).
    *   `Config`: Configura la creación del modelo a partir de atributos.

*   **Clase `ConversionResponse`**: Modelo para la respuesta de la conversión EPUB a PDF.
    *   `download_url: str`: URL de descarga del PDF.

*   **Clase `RagUploadResponse`**: Modelo para la respuesta de la carga de un libro para RAG.
    *   `book_id: str`: ID del libro.
    *   `message: str`: Mensaje de estado.

*   **Clase `RagQuery`**: Modelo para la consulta al sistema RAG.
    *   `query: str`: Consulta del usuario.
    *   `book_id: str`: ID del libro.

*   **Clase `RagQueryResponse`**: Modelo para la respuesta del sistema RAG.
    *   `response: str`: Respuesta generada.


### backend/crud.py

Este archivo contiene la lógica de acceso a datos (CRUD) para la base de datos.

*   `get_book_by_path(db: Session, file_path: str)`: Obtiene un libro por su ruta de archivo. Retorna un objeto `models.Book` o `None`.
*   `get_book_by_title(db: Session, title: str)`: Obtiene un libro por su título exacto. Retorna un objeto `models.Book` o `None`.
*   `get_books_by_partial_title(db: Session, title: str, skip: int = 0, limit: int = 100)`: Busca libros por un título parcial (case-insensitive). Retorna una lista de objetos `models.Book`.
*   `get_books(db: Session, category: str | None = None, search: str | None = None, author: str | None = None)`: Obtiene una lista de libros con opciones de filtrado. Retorna una lista de objetos `models.Book`.
*   `get_categories(db: Session) -> list[str]`: Obtiene una lista de todas las categorías de libros únicas. Retorna una lista de strings.
*   `create_book(db: Session, title: str, author: str, category: str, cover_image_url: str, file_path: str)`: Crea un nuevo libro en la base de datos. Retorna el objeto `models.Book` creado.
*   `delete_book(db: Session, book_id: int)`: Elimina un libro de la base de datos por su ID, incluyendo sus archivos asociados. Retorna el objeto `models.Book` eliminado o `None`.
*   `delete_books_by_category(db: Session, category: str)`: Elimina todos los libros de una categoría específica, incluyendo sus archivos asociados.  Retorna el número de libros eliminados.
*   `get_books_count(db: Session) -> int`: Obtiene el número total de libros en la base de datos. Retorna un entero.


### backend/database.py

Este archivo configura la conexión a la base de datos SQLite.

*   `engine`: Instancia de `create_engine` para la base de datos SQLite.
*   `SessionLocal`: Instancia de `sessionmaker` para crear sesiones de la base de datos.
*   `Base`: Instancia de `declarative_base` para definir los modelos SQLAlchemy.


### backend/models.py

Este archivo define el modelo de datos SQLAlchemy para la tabla `books`.

*   **Clase `Book`**: Modelo SQLAlchemy para la tabla `books`.
    *   `id`: Campo entero, clave primaria, autoincremental.
    *   `title`: Campo string, índice.
    *   `author`: Campo string, índice.
    *   `category`: Campo string, índice.
    *   `cover_image_url`: Campo string, nullable.
    *   `file_path`: Campo string, único.


### backend/rag.py

Este archivo implementa la lógica del sistema RAG.

*   `get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT")`: Genera un embedding para el texto dado usando la API de Google Generative AI. Retorna una lista que representa el embedding.
*   `extract_text_from_pdf(file_path: str) -> str`: Extrae texto de un archivo PDF. Retorna una cadena de texto.
*   `extract_text_from_epub(file_path: str) -> str`: Extrae texto de un archivo EPUB. Retorna una cadena de texto.
*   `chunk_text(text: str, max_tokens: int = 1000) -> list[str]`: Divide el texto en fragmentos más pequeños. Retorna una lista de cadenas de texto.
*   `process_book_for_rag(file_path: str, book_id: str)`: Procesa un libro para el sistema RAG: extrae texto, lo divide en fragmentos, genera embeddings y los almacena en ChromaDB.
*   `query_rag(query: str, book_id: str)`: Consulta el sistema RAG para obtener respuestas basadas en el contenido del libro. Retorna una cadena de texto con la respuesta.


### backend/main.py

Este archivo define las rutas de la API FastAPI.  Contiene las funciones controladoras para cada endpoint.  Se describen las funciones más relevantes aquí:

*   `/upload-book/`: Recibe un archivo de libro (PDF o EPUB), lo procesa usando Gemini para obtener título, autor y categoría, y lo guarda en la base de datos.
*   `/books/`:  Devuelve una lista de libros, con opciones de filtrado por categoría, búsqueda y autor.
*   `/books/count`: Devuelve el número total de libros.
*   `/books/search/`: Busca libros por un título parcial.
*   `/categories/`: Devuelve una lista de categorías únicas.
*   `/books/{book_id}`: Elimina un libro específico.
*   `/categories/{category_name}`: Elimina una categoría y todos sus libros.
*   `/books/download/{book_id}`: Permite descargar un libro.
*   `/tools/convert-epub-to-pdf`: Convierte un archivo EPUB a PDF usando WeasyPrint.
*   `/rag/upload-book/`: Sube un libro para ser procesado por el sistema RAG.
*   `/rag/query/`: Realiza una consulta al sistema RAG.


## 4. Análisis Detallado del Frontend (React)

### frontend/src/App.js

Componente principal de la aplicación React, que define las rutas de navegación utilizando `react-router-dom`.


### frontend/src/Header.js

Componente que muestra el encabezado de la aplicación, incluyendo la navegación y un contador de libros.

*   **Estado**: `menuOpen`, `bookCount`, `errorMessage`.
*   **Efectos**: Obtiene el número de libros del backend y actualiza el contador periódicamente.
*   **Interacción con el usuario**: Botón de menú hamburguesa para abrir y cerrar la navegación.
*   **Comunicación con el backend**: Realiza una petición `fetch` a `/books/count` para obtener el número de libros.


### frontend/src/LibraryView.js

Componente que muestra la lista de libros.

*   **Estado**: `books`, `searchTerm`, `error`, `loading`, `isMobile`.
*   **Efectos**: Obtiene la lista de libros del backend, maneja el debounce de la búsqueda.
*   **Interacción con el usuario**: Campo de búsqueda, botones para eliminar libros.
*   **Comunicación con el backend**: Realiza una petición `fetch` a `/books/` con parámetros de búsqueda y filtrado.


### frontend/src/UploadView.js

Componente para subir libros.

*   **Estado**: `filesToUpload`, `isUploading`.
*   **Interacción con el usuario**: Permite seleccionar y arrastrar archivos, botón para iniciar la subida.
*   **Comunicación con el backend**: Envía los archivos a `/upload-book/` usando `fetch` y actualiza el estado de cada archivo durante el proceso de subida.


### frontend/src/ToolsView.js

Componente que contiene el convertidor EPUB a PDF.

*   **Estado**: `selectedFile`, `message`, `isLoading`.
*   **Interacción con el usuario**: Permite seleccionar un archivo EPUB, botón para iniciar la conversión.
*   **Comunicación con el backend**: Realiza una petición `POST` a `/tools/convert-epub-to-pdf` para la conversión y maneja la descarga del PDF generado.


### frontend/src/ReaderView.js

Componente que muestra el lector de libros EPUB.

*   **Estado**: `location`, `epubData`, `isLoading`, `error`.
*   **Interacción con el usuario**: Permite la navegación dentro del libro.
*   **Comunicación con el backend**: Obtiene el libro (EPUB) usando `fetch` en `/books/download/${bookId}`


### frontend/src/RagView.js

Componente para la interacción con el sistema RAG.

*   **Estado**: `selectedFile`, `message`, `isLoading`, `bookId`, `chatHistory`, `currentQuery`.
*   **Interacción con el usuario**: Permite seleccionar un archivo, hacer preguntas a través de un formulario.
*   **Comunicación con el backend**: Realiza peticiones `POST` a `/rag/upload-book/` para subir el libro y a `/rag/query/` para realizar las consultas al sistema RAG.


### frontend/src/CategoriesView.js

Componente para mostrar las categorías de libros.

*   **Estado**: `categories`, `error`, `loading`.
*   **Comunicación con el backend**: Obtiene las categorías desde el endpoint `/categories/`.


## 5. Flujo de Datos y API

1.  El usuario selecciona un archivo de libro (PDF o EPUB) en el componente `UploadView`.
2.  El frontend envía el archivo al backend a través de una petición `POST` a `/upload-book/`.
3.  El backend procesa el archivo, extrae texto (si es necesario), utiliza Gemini para analizar las primeras páginas para obtener el título, autor y categoría.
4.  El backend guarda la información del libro (incluyendo la ruta del archivo) en la base de datos.
5.  El backend retorna los detalles del libro al frontend.
6.  El frontend actualiza la lista de libros en `LibraryView`.
7.  Para consultar el sistema RAG:
    *   El usuario sube un libro a través de `/rag/upload-book/`.
    *   El backend procesa el libro y guarda los embeddings en ChromaDB.
    *   El usuario realiza consultas a través de `/rag/query/`.
    *   El backend consulta ChromaDB, recupera los fragmentos relevantes y utiliza Gemini para generar una respuesta.
    *   El backend devuelve la respuesta al frontend.


**Principales Endpoints de la API:**

*   `/upload-book/` (POST): Subir un libro.
*   `/books/` (GET): Obtener libros (con opciones de filtrado).
*   `/books/count` (GET): Obtener el conteo de libros.
*   `/books/search/` (GET): Buscar libros por título parcial.
*   `/categories/` (GET): Obtener categorías.
*   `/books/{book_id}` (DELETE): Eliminar un libro.
*   `/categories/{category_name}` (DELETE): Eliminar una categoría.
*   `/books/download/{book_id}` (GET): Descargar un libro.
*   `/tools/convert-epub-to-pdf` (POST): Convertir EPUB a PDF.
*   `/rag/upload-book/` (POST): Subir libro para RAG.
*   `/rag/query/` (POST): Consultar RAG.

