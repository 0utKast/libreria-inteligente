# DOCUMENTACION_PROYECTO.md

## 1. Descripción General del Proyecto

"Mi Librería Inteligente" es una aplicación web que permite a los usuarios gestionar su colección de libros digitales.  La aplicación ofrece funcionalidades para subir libros (PDF y EPUB), buscar libros por título, autor o categoría,  eliminar libros, convertir EPUB a PDF y consultar sobre el contenido de los libros mediante un sistema de Recuperación de Información basada en Representaciones (RAG).

La arquitectura de la aplicación se basa en un frontend desarrollado con React, un backend construido con FastAPI (Python) y una base de datos SQLite para el almacenamiento persistente de información de los libros.  La comunicación entre el frontend y el backend se realiza mediante una API REST. El sistema RAG utiliza Google Gemini para generar embeddings y responder preguntas.


## 2. Estructura del Proyecto

El proyecto está organizado en dos directorios principales: `backend/` y `frontend/`.

*   **`backend/`:** Contiene el código del backend de la aplicación, incluyendo:
    *   **`schemas.py`:** Define los modelos Pydantic para la validación y serialización de datos.
    *   **`crud.py`:**  Contiene la lógica de acceso a datos (CRUD) para la interacción con la base de datos.
    *   **`database.py`:** Configura la conexión a la base de datos SQLite.
    *   **`models.py`:** Define el modelo de datos SQLAlchemy para la tabla `books`.
    *   **`rag.py`:** Implementa la lógica del sistema RAG, utilizando Google Gemini y ChromaDB.
    *   **`main.py`:** El archivo principal del backend, que define las rutas de la API FastAPI.
    *   **`alembic/`:** Directorio para las migraciones de la base de datos.

*   **`frontend/src/`:** Contiene el código fuente del frontend React, incluyendo componentes para la interfaz de usuario.


## 3. Análisis Detallado del Backend (Python/FastAPI)

### `backend/schemas.py`

Este archivo define los modelos de datos Pydantic utilizados para la serialización y validación de datos en la API FastAPI.

*   **`BookBase`:** Modelo base para un libro, que incluye los campos `title`, `author`, `category`, `cover_image_url` (opcional) y `file_path`.
*   **`Book`:**  Hereda de `BookBase` y añade el campo `id` (entero).  `from_attributes = True` permite la creación de instancias a partir de atributos.
*   **`ConversionResponse`:** Modelo para la respuesta de la conversión EPUB a PDF, con el campo `download_url`.
*   **`RagUploadResponse`:** Modelo para la respuesta de la subida de un libro para RAG, con los campos `book_id` y `message`.
*   **`RagQuery`:** Modelo para la petición de consulta RAG, con los campos `query` y `book_id`.
*   **`RagQueryResponse`:** Modelo para la respuesta de consulta RAG, con el campo `response`.


### `backend/crud.py`

Este archivo contiene las funciones para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los libros en la base de datos.

*   `get_book_by_path(db: Session, file_path: str)`: Obtiene un libro por su ruta de archivo. Retorna un objeto `models.Book` o `None`.
*   `get_book_by_title(db: Session, title: str)`: Obtiene un libro por su título exacto. Retorna un objeto `models.Book` o `None`.
*   `get_books_by_partial_title(db: Session, title: str, skip: int = 0, limit: int = 100)`: Busca libros por un título parcial (case-insensitive), con paginación. Retorna una lista de objetos `models.Book`.
*   `get_books(db: Session, category: str | None = None, search: str | None = None, author: str | None = None)`: Obtiene una lista de libros, con opciones de filtrado por categoría, búsqueda general y autor. Retorna una lista de objetos `models.Book`.
*   `get_categories(db: Session) -> list[str]`: Obtiene una lista de todas las categorías únicas. Retorna una lista de strings.
*   `create_book(db: Session, title: str, author: str, category: str, cover_image_url: str, file_path: str)`: Crea un nuevo libro en la base de datos. Retorna el objeto `models.Book` recién creado.
*   `delete_book(db: Session, book_id: int)`: Elimina un libro de la base de datos por su ID, incluyendo sus archivos asociados. Retorna el objeto `models.Book` eliminado o `None`.
*   `delete_books_by_category(db: Session, category: str)`: Elimina todos los libros de una categoría específica, incluyendo sus archivos asociados. Retorna el número de libros eliminados.
*   `get_books_count(db: Session) -> int`: Obtiene el número total de libros en la base de datos. Retorna un entero.


### `backend/database.py`

Este archivo configura la conexión a la base de datos SQLite utilizando SQLAlchemy.  Define `engine` y `SessionLocal`.


### `backend/models.py`

Este archivo define el modelo de datos SQLAlchemy para la tabla `books`.

*   **`Book`:**  Define la estructura de la tabla `books` con los campos: `id` (Integer, primary key), `title` (String), `author` (String), `category` (String), `cover_image_url` (String, nullable=True), y `file_path` (String, unique=True).


### `backend/rag.py`

Este archivo implementa la lógica para el sistema RAG.

*   `get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT")`: Genera un embedding para el texto dado usando Google Gemini. Retorna una lista que representa el embedding.
*   `extract_text_from_pdf(file_path: str) -> str`: Extrae texto de un archivo PDF. Retorna una cadena de texto.
*   `extract_text_from_epub(file_path: str) -> str`: Extrae texto de un archivo EPUB. Retorna una cadena de texto.
*   `chunk_text(text: str, max_tokens: int = 1000) -> list[str]`: Divide el texto en fragmentos más pequeños. Retorna una lista de cadenas de texto.
*   `process_book_for_rag(file_path: str, book_id: str)`: Procesa un libro para RAG: extrae texto, lo divide en fragmentos, genera embeddings y los almacena en ChromaDB. No retorna nada.
*   `query_rag(query: str, book_id: str)`: Consulta el sistema RAG para obtener respuestas. Retorna una cadena de texto con la respuesta.


### `backend/main.py`

Este archivo es el punto de entrada de la aplicación FastAPI. Define las rutas de la API.  Incluye la lógica para procesar archivos PDF y EPUB, usar Google Gemini para el análisis inicial y manejar la subida, descarga y eliminación de libros.


## 4. Análisis Detallado del Frontend (React)

### `frontend/src/Header.js`

Componente que representa el encabezado de la aplicación.  Muestra el logo, el contador de libros, el menú de navegación y maneja el estado de apertura/cierre del menú.  Realiza peticiones al backend para obtener el contador de libros.


### `frontend/src/App.js`

Componente principal de la aplicación React que configura las rutas utilizando `react-router-dom`.


### `frontend/src/ToolsView.js`

Componente que presenta las herramientas disponibles en la aplicación. Actualmente solo incluye el convertidor de EPUB a PDF.  Maneja la subida de archivos, la comunicación con el backend y la descarga del archivo convertido.


### `frontend/src/UploadView.js`

Componente para subir libros a la biblioteca.  Maneja la subida de múltiples archivos, muestra el estado de subida de cada archivo y actualiza la interfaz de usuario según el progreso.  Realiza peticiones POST al backend para subir y procesar los libros.


### `frontend/src/ReaderView.js`

Componente que muestra un libro EPUB utilizando la librería `react-reader`.  Realiza una petición al backend para descargar el libro y lo renderiza utilizando la librería.


### `frontend/src/RagView.js`

Componente que implementa la interfaz para interactuar con el sistema RAG.  Permite subir un libro, hacer preguntas sobre su contenido y muestra las respuestas de la IA.


### `frontend/src/LibraryView.js`

Componente principal para mostrar la biblioteca.  Muestra los libros cargados, maneja la búsqueda y la eliminación de libros.  Realiza peticiones GET al backend para obtener los datos de los libros y peticiones DELETE para eliminarlos.


### `frontend/src/config.js`

Archivo que contiene la URL de la API del backend.


### `frontend/src/CategoriesView.js`

Componente para mostrar la lista de categorías.  Realiza peticiones al backend para obtener las categorías y las muestra en pantalla.


## 5. Flujo de Datos y API

1.  **Subida de libro (Frontend):** El usuario selecciona un archivo (PDF o EPUB) en `UploadView.js` y lo envía al backend mediante una petición POST a `/upload-book/`.
2.  **Procesamiento en Backend (`main.py`):** El backend recibe el archivo, lo procesa (extrae texto y portada si es posible), usa Google Gemini para determinar el título, autor y categoría y luego crea un nuevo registro en la base de datos a través de `crud.create_book()`.
3.  **Almacenamiento en la base de datos:** La información del libro (junto con su ruta de archivo) se almacena en la tabla `books` en la base de datos SQLite.
4.  **Visualización en el frontend:** `LibraryView.js` realiza una petición GET a `/books/` para obtener la lista de libros.  Los libros se muestran en la interfaz de usuario.
5.  **Búsqueda y Filtrado:**  Las búsquedas se realizan mediante peticiones GET a `/books/` con parámetros de consulta (`category`, `search`, `author`).
6.  **Eliminación de libros:** Se realiza una petición DELETE a `/books/{book_id}` para eliminar un libro.  El backend elimina el registro de la base de datos y el archivo correspondiente.
7.  **Conversión EPUB a PDF:**  El usuario sube un archivo EPUB mediante una petición POST a `/tools/convert-epub-to-pdf`.  El backend realiza la conversión usando `WeasyPrint` y devuelve una URL para descargar el PDF.
8.  **RAG (Sistema de Preguntas y Respuestas):** El usuario puede subir un libro a `/rag/upload-book/`. El backend procesa el libro mediante `rag.process_book_for_rag()`, genera embeddings y almacena los datos en ChromaDB.  El usuario puede luego hacer preguntas mediante peticiones POST a `/rag/query/`, recibiendo las respuestas del modelo de lenguaje Gemini.

**Endpoints de la API:**

*   `/upload-book/` (POST): Subir un libro.
*   `/books/` (GET): Obtener lista de libros (con opciones de filtrado).
*   `/books/count` (GET): Obtener el número total de libros.
*   `/books/search/` (GET): Buscar libros por título parcial.
*   `/categories/` (GET): Obtener lista de categorías.
*   `/books/{book_id}` (DELETE): Eliminar un libro.
*   `/categories/{category_name}` (DELETE): Eliminar una categoría y sus libros.
*   `/books/download/{book_id}` (GET): Descargar un libro.
*   `/tools/convert-epub-to-pdf` (POST): Convertir EPUB a PDF.
*   `/rag/upload-book/` (POST): Subir libro para RAG.
*   `/rag/query/` (POST): Consultar RAG.

