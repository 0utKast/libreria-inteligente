# DOCUMENTACION_PROYECTO.md

## 1. Descripción General del Proyecto

"Mi Librería Inteligente" es una aplicación web que permite a los usuarios gestionar su colección de libros digitalmente.  La aplicación ofrece funcionalidades para subir libros (PDF y EPUB), visualizarlos en una biblioteca organizada por categorías y autores, realizar búsquedas, convertir EPUB a PDF y consultar la información de un libro usando un sistema de Recuperación de Información basada en Conocimiento (RAG).

La aplicación utiliza una arquitectura cliente-servidor: un frontend desarrollado con React se encarga de la interfaz de usuario y la interacción con el usuario, mientras que un backend en FastAPI (Python) se encarga del procesamiento de datos, la gestión de la base de datos y la lógica de la aplicación.  La base de datos es una base de datos SQLite.  El RAG utiliza Gemini de Google para generar embeddings y respuestas.


## 2. Estructura del Proyecto

El proyecto se divide en dos partes principales: el backend (Python) y el frontend (React).

*   **backend/:** Contiene el código del backend de FastAPI, incluyendo:
    *   **database.py:**  Configuración de la base de datos SQLAlchemy.
    *   **models.py:** Definición del modelo de datos para libros (esquema de la base de datos).
    *   **schemas.py:** Definición de los esquemas Pydantic para la serialización y validación de datos.
    *   **crud.py:**  Funciones CRUD (Create, Read, Update, Delete) para interactuar con la base de datos.
    *   **main.py:**  El punto de entrada de la aplicación FastAPI, que define las rutas y la lógica de la API.
    *   **rag.py:** Lógica para el procesamiento de libros para el sistema RAG (extracción de texto, creación de embeddings, consulta).
    *   **alembic/:**  Directorio para las migraciones de la base de datos.

*   **frontend/src/:** Contiene el código fuente del frontend de React, organizado en componentes:
    *   **App.js:** Componente principal que gestiona el enrutamiento.
    *   **Header.js:** Componente para el encabezado de la aplicación, incluyendo la navegación.
    *   **LibraryView.js:** Componente para visualizar la lista de libros.
    *   **UploadView.js:** Componente para subir libros nuevos.
    *   **CategoriesView.js:** Componente para visualizar las categorías de libros.
    *   **ToolsView.js:** Componente para mostrar las herramientas disponibles, como el conversor de EPUB a PDF.
    *   **RagView.js:** Componente para interactuar con el sistema RAG.
    *   **ReaderView.js:** Componente para leer archivos EPUB utilizando `react-reader`.
    *   **config.js:** URL de la API backend.


## 3. Análisis Detallado del Backend (Python/FastAPI)

### 3.1 backend/database.py

*   **Propósito:** Configura la conexión a la base de datos SQLite utilizando SQLAlchemy.
*   **Variables:**
    *   `SQLALCHEMY_DATABASE_URL`: URL de conexión a la base de datos (SQLite).
    *   `engine`:  Motor de la base de datos SQLAlchemy.
    *   `SessionLocal`:  Generador de sesiones SQLAlchemy.
    *   `Base`:  Base declarativa de SQLAlchemy.

### 3.2 backend/models.py

*   **Propósito:** Define el modelo de datos `Book` para la base de datos.
*   **Clase `Book`:**
    *   `id`:  Clave primaria (Integer).
    *   `title`:  Título del libro (String).
    *   `author`:  Autor del libro (String).
    *   `category`:  Categoría del libro (String).
    *   `cover_image_url`:  URL de la imagen de portada (String, nullable=True).
    *   `file_path`:  Ruta al archivo del libro (String, unique=True).

### 3.3 backend/schemas.py

*   **Propósito:** Define los esquemas Pydantic para la serialización y validación de datos.
*   **Clases:**
    *   `BookBase`:  Esquema base para la creación de libros.
    *   `Book`:  Esquema completo para los libros, incluyendo el ID.
    *   `ConversionResponse`:  Respuesta para la conversión de EPUB a PDF.
    *   `RagUploadResponse`:  Respuesta para la subida de libros a RAG.
    *   `RagQuery`:  Esquema de solicitud para consultas RAG.
    *   `RagQueryResponse`:  Respuesta para consultas RAG.

### 3.4 backend/crud.py

*   **Propósito:**  Implementa las funciones CRUD para la gestión de libros.
*   **Funciones:**
    *   `get_book_by_path(db: Session, file_path: str)`: Obtiene un libro por su ruta de archivo.
    *   `get_book_by_title(db: Session, title: str)`: Obtiene un libro por su título exacto.
    *   `get_books_by_partial_title(db: Session, title: str, skip: int = 0, limit: int = 100)`: Busca libros por título parcial (case-insensitive).
    *   `get_books(db: Session, category: str | None = None, search: str | None = None, author: str | None = None)`: Obtiene libros con filtros opcionales.
    *   `get_categories(db: Session) -> list[str]`: Obtiene una lista de categorías únicas.
    *   `create_book(db: Session, title: str, author: str, category: str, cover_image_url: str, file_path: str)`: Crea un nuevo libro.
    *   `delete_book(db: Session, book_id: int)`: Elimina un libro por su ID, incluyendo archivos.
    *   `delete_books_by_category(db: Session, category: str)`: Elimina libros de una categoría, incluyendo archivos.
    *   `get_books_count(db: Session) -> int`: Obtiene el número total de libros.

### 3.5 backend/rag.py

*   **Propósito:**  Implementa la lógica para el sistema RAG.
*   **Funciones:**
    *   `get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT")`: Genera un embedding para el texto dado utilizando Gemini.
    *   `extract_text_from_pdf(file_path: str) -> str`: Extrae texto de un archivo PDF.
    *   `extract_text_from_epub(file_path: str) -> str`: Extrae texto de un archivo EPUB.
    *   `chunk_text(text: str, max_tokens: int = 1000) -> list[str]`: Divide el texto en fragmentos.
    *   `process_book_for_rag(file_path: str, book_id: str)`: Procesa un libro para RAG (extracción, fragmentación, embeddings, almacenamiento en ChromaDB).
    *   `query_rag(query: str, book_id: str)`: Consulta el sistema RAG para obtener respuestas.

### 3.6 backend/main.py

*   **Propósito:** Define las rutas y la lógica de la API FastAPI.
*   **Rutas:**
    *   `/upload-book/`:  Sube un libro.
    *   `/books/`:  Obtiene libros con filtros opcionales.
    *   `/books/count`: Obtiene el número total de libros.
    *   `/books/search/`: Busca libros por título parcial.
    *   `/categories/`: Obtiene las categorías de libros.
    *   `/books/{book_id}`: Elimina un libro por ID.
    *   `/categories/{category_name}`: Elimina una categoría y sus libros.
    *   `/books/download/{book_id}`: Descarga un libro.
    *   `/tools/convert-epub-to-pdf`: Convierte un EPUB a PDF.
    *   `/rag/upload-book/`: Sube un libro para RAG.
    *   `/rag/query/`: Consulta el sistema RAG.


## 4. Análisis Detallado del Frontend (React)

### 4.1 frontend/src/App.js

*   **Propósito:** Componente principal, gestiona el enrutamiento utilizando `react-router-dom`.
*   **Estado:** No tiene estado propio.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:** No realiza interacciones directas con el backend.

### 4.2 frontend/src/Header.js

*   **Propósito:** Componente para el encabezado y la navegación de la aplicación.
*   **Estado:**
    *   `menuOpen`:  Controla la apertura y cierre del menú.
    *   `bookCount`:  Número total de libros (obtenido del backend).
    *   `errorMessage`: Mensaje de error para la carga del contador de libros.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:**  Realiza una petición a `/books/count` para obtener el número total de libros.

### 4.3 frontend/src/LibraryView.js

*   **Propósito:** Visualiza la lista de libros, con opciones de búsqueda y filtrado.
*   **Estado:**
    *   `books`:  Lista de libros.
    *   `searchTerm`: Término de búsqueda actual.
    *   `error`: Mensaje de error.
    *   `loading`: Indica si se están cargando datos.
    *   `isMobile`: Detecta si la interfaz está en un dispositivo móvil.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:**  Realiza peticiones a `/books/` para obtener los libros, con parámetros de búsqueda y filtrado.  También realiza peticiones DELETE a `/books/{bookId}`.

### 4.4 frontend/src/UploadView.js

*   **Propósito:** Permite a los usuarios subir libros.
*   **Estado:**
    *   `filesToUpload`:  Un array de objetos que describen el estado de cada archivo subido.
    *   `isUploading`:  Indica si se está subiendo algún archivo.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:**  Realiza peticiones POST a `/upload-book/` para subir cada archivo.

### 4.5 frontend/src/CategoriesView.js

*   **Propósito:** Muestra una lista de categorías de libros.
*   **Estado:**
    *   `categories`:  Lista de categorías.
    *   `error`: Mensaje de error.
    *   `loading`: Indica si se están cargando datos.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:**  Realiza una petición a `/categories/` para obtener la lista de categorías.

### 4.6 frontend/src/ToolsView.js

*   **Propósito:**  Proporciona herramientas, incluyendo la conversión de EPUB a PDF.
*   **Estado:**
    *   `selectedFile`: El archivo EPUB seleccionado.
    *   `message`:  Mensaje para mostrar al usuario.
    *   `isLoading`: Indica si se está realizando la conversión.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:** Realiza peticiones POST a `/tools/convert-epub-to-pdf` para convertir archivos.

### 4.7 frontend/src/RagView.js

*   **Propósito:** Permite la interacción con el sistema RAG.
*   **Estado:**
    *   `selectedFile`:  Archivo seleccionado para procesar.
    *   `message`: Mensaje para el usuario.
    *   `isLoading`: Indica si hay algún proceso en ejecución.
    *   `bookId`: ID del libro procesado para RAG.
    *   `chatHistory`: Historial del chat.
    *   `currentQuery`: Consulta actual.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:**  Realiza peticiones POST a `/rag/upload-book/` y `/rag/query/`.

### 4.8 frontend/src/ReaderView.js

*   **Propósito:**  Muestra un lector de libros EPUB.
*   **Estado:**
    *   `location`:  Ubicación actual en el libro.
    *   `epubData`: Datos del EPUB (arrayBuffer).
    *   `isLoading`: Estado de carga.
    *   `error`: Mensaje de error.
*   **Propiedades:** No tiene propiedades propias.
*   **Interacción con el Backend:** Realiza peticiones GET a `/books/download/{bookId}` para descargar el libro.

### 4.9 frontend/src/config.js
* **Propósito:**  Define la URL base de la API del backend.
* **Variable:** `API_URL`


## 5. Flujo de Datos y API

El flujo de datos comienza con el usuario subiendo un libro (PDF o EPUB) en `UploadView.js`.  El frontend envía el archivo al endpoint `/upload-book/` del backend.  El backend procesa el archivo (extrae texto, identifica metadata, guarda el archivo), y guarda los datos del libro en la base de datos.  La información del libro se devuelve al frontend, actualizando la lista de libros en `LibraryView.js`.

La búsqueda de libros se realiza enviando parámetros (search, category, author) al endpoint `/books/`, que devuelve los resultados filtrados.  El lector EPUB en `ReaderView.js` descarga el libro a través del endpoint `/books/download/{book_id}`.  La conversión EPUB a PDF utiliza el endpoint `/tools/convert-epub-to-pdf`.  El sistema RAG recibe libros a través de `/rag/upload-book/` y procesa consultas con `/rag/query/`.


Los principales endpoints de la API son:

*   `/upload-book/` (POST): Sube un libro.
*   `/books/` (GET): Obtiene libros, con opciones de filtrado.
*   `/books/count` (GET): Obtiene el número total de libros.
*   `/books/search/` (GET): Busca libros por título parcial.
*   `/categories/` (GET): Obtiene categorías.
*   `/books/{book_id}` (DELETE): Elimina un libro.
*   `/categories/{category_name}` (DELETE): Elimina una categoría y sus libros.
*   `/books/download/{book_id}` (GET): Descarga un libro.
*   `/tools/convert-epub-to-pdf` (POST): Convierte EPUB a PDF.
*   `/rag/upload-book/` (POST): Sube libro para RAG.
*   `/rag/query/` (POST): Consulta RAG.

