# DOCUMENTACION_PROYECTO.md

## 1. Descripción General del Proyecto

"Mi Librería Inteligente" es una aplicación web que permite a los usuarios gestionar su colección de libros digitalmente.  La aplicación permite subir libros en formato PDF y EPUB, los analiza para extraer metadatos (título, autor, categoría), los almacena en una base de datos y proporciona una interfaz para buscar, visualizar y gestionar la colección.  Además, incluye un conversador basado en RAG (Retrieval Augmented Generation) que permite al usuario realizar consultas sobre el contenido de los libros subidos.

La arquitectura de la aplicación se basa en una estructura cliente-servidor. El frontend está desarrollado con React y se encarga de la interfaz de usuario y la interacción con el usuario. El backend, construido con FastAPI (Python), gestiona la lógica del negocio, el almacenamiento de datos y la interacción con la API de Gemini de Google para el análisis de los libros.  Se utiliza una base de datos SQLite para persistir la información de los libros.  El sistema RAG se basa en ChromaDB para la gestión de embeddings y la API de Gemini para la generación de respuestas.


## 2. Estructura del Proyecto

El proyecto se divide en dos partes principales: el backend (Python) y el frontend (React).

*   **backend/**: Contiene todo el código del backend de la aplicación.
    *   **alembic/**:  Contiene las migraciones de la base de datos.
    *   **schemas.py**: Define los esquemas Pydantic para la serialización y deserialización de datos.
    *   **crud.py**: Contiene la lógica de acceso a datos (CRUD) para la base de datos.
    *   **database.py**: Configura la conexión a la base de datos SQLite.
    *   **models.py**: Define el modelo de datos SQLAlchemy para la tabla de libros.
    *   **rag.py**:  Implementa la lógica para el sistema RAG (Retrieval Augmented Generation).
    *   **main.py**:  El punto de entrada de la aplicación FastAPI.

*   **frontend/**: Contiene todo el código del frontend de la aplicación.
    *   **src/**: Contiene el código fuente de la aplicación React.
        *   **App.js**: El componente principal de la aplicación React.
        *   **Header.js**: Componente para el encabezado de la aplicación.
        *   **LibraryView.js**: Componente para mostrar la biblioteca de libros.
        *   **UploadView.js**: Componente para subir libros.
        *   **CategoriesView.js**: Componente para visualizar las categorías de libros.
        *   **ToolsView.js**: Componente para las herramientas de la aplicación (conversor EPUB a PDF).
        *   **ReaderView.js**: Componente para leer libros en formato EPUB.
        *   **RagView.js**: Componente para la interacción con el sistema RAG.
        *   **config.js**: Archivo de configuración con la URL de la API.


## 3. Análisis Detallado del Backend (Python/FastAPI)

### backend/schemas.py

Este archivo define los modelos Pydantic para la serialización y deserialización de datos JSON en la API.

*   **`BookBase`**: Modelo base para la creación de un libro.
    *   `title: str`: Título del libro (requerido).
    *   `author: str`: Autor del libro (requerido).
    *   `category: str`: Categoría del libro (requerido).
    *   `cover_image_url: str | None = None`: URL de la imagen de portada (opcional).
    *   `file_path: str`: Ruta al archivo del libro (requerido).

*   **`Book`**: Modelo para representar un libro incluyendo su ID. Hereda de `BookBase`.
    *   `id: int`: ID del libro (requerido).

*   **`ConversionResponse`**: Modelo para la respuesta de la conversión EPUB a PDF.
    *   `download_url: str`: URL de descarga del PDF generado.

*   **`RagUploadResponse`**:  Modelo para la respuesta de la subida de un libro para RAG.
    *   `book_id: str`: ID del libro procesado para RAG.
    *   `message: str`: Mensaje de confirmación o error.

*   **`RagQuery`**: Modelo para la solicitud de consulta al sistema RAG.
    *   `query: str`: La consulta del usuario.
    *   `book_id: str`: El ID del libro al que se refiere la consulta.

*   **`RagQueryResponse`**: Modelo para la respuesta de una consulta al sistema RAG.
    *   `response: str`: La respuesta generada por el modelo.


### backend/crud.py

Este archivo contiene la lógica de acceso a datos (CRUD) para la base de datos.

*   **`get_book_by_path(db: Session, file_path: str)`**: Obtiene un libro por su ruta de archivo. Retorna un objeto `models.Book` o `None`.
*   **`get_book_by_title(db: Session, title: str)`**: Obtiene un libro por su título exacto. Retorna un objeto `models.Book` o `None`.
*   **`get_books_by_partial_title(db: Session, title: str, skip: int = 0, limit: int = 100)`**: Busca libros por un título parcial (case-insensitive). Retorna una lista de objetos `models.Book`.
*   **`get_books(db: Session, category: str | None = None, search: str | None = None, author: str | None = None)`**: Obtiene una lista de libros, con opciones de filtrado por categoría, búsqueda general y autor. Retorna una lista de objetos `models.Book`.
*   **`get_categories(db: Session) -> list[str]`**: Obtiene una lista de todas las categorías de libros únicas. Retorna una lista de strings.
*   **`create_book(db: Session, title: str, author: str, category: str, cover_image_url: str, file_path: str)`**: Crea un nuevo libro en la base de datos. Retorna un objeto `models.Book`.
*   **`delete_book(db: Session, book_id: int)`**: Elimina un libro de la base de datos por su ID, incluyendo sus archivos asociados. Retorna el objeto `models.Book` eliminado o `None`.
*   **`delete_books_by_category(db: Session, category: str)`**: Elimina todos los libros de una categoría específica, incluyendo sus archivos asociados. Retorna el número de libros eliminados.
*   **`get_books_count(db: Session) -> int`**: Obtiene el número total de libros en la base de datos. Retorna un entero.


### backend/database.py

Este archivo configura la conexión a la base de datos SQLite.  Define `engine` y `SessionLocal` para la interacción con la base de datos.


### backend/models.py

Este archivo define el modelo de datos SQLAlchemy para la tabla de libros.

*   **`Book`**: Modelo SQLAlchemy para la tabla "books".
    *   `id`: Clave primaria, entero.
    *   `title`: String, índice.
    *   `author`: String, índice.
    *   `category`: String, índice.
    *   `cover_image_url`: String, nullable.
    *   `file_path`: String, único.


### backend/rag.py

Este archivo implementa la lógica para el sistema RAG.

*   **`get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT")`**: Genera un embedding para el texto dado usando la API de Gemini. Retorna una lista que representa el embedding.
*   **`extract_text_from_pdf(file_path: str) -> str`**: Extrae texto de un archivo PDF. Retorna un string con el texto extraído.
*   **`extract_text_from_epub(file_path: str) -> str`**: Extrae texto de un archivo EPUB. Retorna un string con el texto extraído.
*   **`chunk_text(text: str, max_tokens: int = 1000) -> list[str]`**: Divide el texto en fragmentos más pequeños basados en el número de tokens. Retorna una lista de strings.
*   **`process_book_for_rag(file_path: str, book_id: str)`**: Procesa un libro para RAG: extrae texto, lo divide en fragmentos, genera embeddings y los almacena en ChromaDB.  No retorna ningún valor.
*   **`query_rag(query: str, book_id: str)`**: Consulta el sistema RAG para obtener respuestas basadas en el contenido del libro. Retorna un string con la respuesta.


### backend/main.py

Este archivo es el punto de entrada de la aplicación FastAPI. Define las rutas de la API y la lógica de procesamiento de los libros.  Las funciones clave ya han sido descritas en las secciones anteriores.


## 4. Análisis Detallado del Frontend (React)

### frontend/src/App.js

Componente principal de la aplicación React.  Define las rutas de navegación usando `react-router-dom`.


### frontend/src/Header.js

Componente para el encabezado de la aplicación.  Muestra el título, un menú de navegación y el contador de libros.  Utiliza un estado (`menuOpen`) para controlar la visibilidad del menú.  El contador de libros se obtiene a través de una petición a la API (`/books/count`) y se actualiza periódicamente con `setInterval`.


### frontend/src/ToolsView.js

Componente que muestra un conversor de EPUB a PDF.  El conversor utiliza un estado (`selectedFile`, `message`, `isLoading`) para controlar la selección de archivos, los mensajes al usuario y el estado de carga. La conversión se realiza mediante una petición POST a la API (`/tools/convert-epub-to-pdf`). El componente incluye lógica para manejar arrastrar y soltar archivos.


### frontend/src/UploadView.js

Componente para subir libros.  Gestiona múltiples subidas de archivos (PDF y EPUB). Utiliza el estado `filesToUpload` para seguir el estado de cada archivo (pendiente, subiendo, éxito o error).  Cada archivo se sube individualmente mediante una petición POST a la API (`/upload-book/`).  Incluye lógica para manejar arrastrar y soltar archivos.


### frontend/src/ReaderView.js

Componente para leer libros en formato EPUB. Recibe el `bookId` como parámetro de la ruta. Obtiene el libro desde la API (`/books/download/{bookId}`) utilizando `fetch` y lo renderiza usando la librería `react-reader`.  Gestiona el estado de carga (`isLoading`) y de error (`error`).


### frontend/src/RagView.js

Este componente se encarga de la interfaz de usuario para la interacción con el sistema RAG.  Permite al usuario subir un libro y hacer preguntas sobre su contenido.  Tiene estado para el archivo seleccionado (`selectedFile`), mensajes al usuario (`message`), estado de carga (`isLoading`), el ID del libro (`bookId`), el historial de chat (`chatHistory`) y la consulta actual (`currentQuery`). La subida del libro se realiza mediante una petición POST a la API (`/rag/upload-book/`), y las consultas se hacen con peticiones POST a `/rag/query/`.


### frontend/src/LibraryView.js

Componente que muestra la lista de libros.  Realiza peticiones a la API (`/books/`) para obtener la lista de libros. Usa `useSearchParams` para manejar la búsqueda y filtrado.  Implementa búsqueda por título, autor y categoría.  Incluye lógica para eliminar libros a través de peticiones DELETE a la API (`/books/{bookId}`).


### frontend/src/config.js

Archivo de configuración que contiene la URL de la API backend.


### frontend/src/CategoriesView.js

Componente que muestra una lista de las categorías de libros. Obtiene los datos de la API (`/categories/`) para visualizar las categorias.



## 5. Flujo de Datos y API

1.  **Subida de Libro (Frontend):** El usuario selecciona o arrastra un archivo (PDF o EPUB) en `UploadView.js`.
2.  **Subida de Libro (Backend):** `UploadView.js` envía una petición POST a `/upload-book/` con el archivo.  `main.py` recibe el archivo, lo procesa (extrae texto y portada), llama a la API de Gemini para obtener metadatos, y guarda la información en la base de datos mediante `crud.py`.
3.  **Visualización de Libros (Frontend):** `LibraryView.js` realiza una petición GET a `/books/` (con parámetros opcionales para búsqueda y filtrado) para obtener la lista de libros.  Muestra los datos en la interfaz.
4.  **Descarga de Libro (Frontend/Backend):** `LibraryView.js` genera un enlace para descargar un libro usando la ruta `/books/download/{book_id}`.  `main.py` devuelve el archivo correspondiente.
5.  **Conversión EPUB a PDF (Frontend/Backend):** `ToolsView.js` envía una petición POST a `/tools/convert-epub-to-pdf`. `main.py` realiza la conversión y devuelve una URL de descarga para el PDF generado.
6.  **RAG:** `RagView.js` envía una petición POST a `/rag/upload-book/` para subir el libro para RAG.  `rag.py` procesa el libro, extrae texto, crea embeddings y los almacena en ChromaDB.  Para consultas, `RagView.js` envía una petición POST a `/rag/query/` con la consulta y el `book_id`. `rag.py` realiza la consulta en ChromaDB y genera una respuesta usando la API de Gemini.


**Endpoints de la API:**

*   `POST /upload-book/`: Subir un libro.
*   `GET /books/`: Obtener lista de libros (con opciones de filtrado).
*   `GET /books/count`: Obtener el número total de libros.
*   `GET /books/search/`: Buscar libros por título parcial.
*   `GET /categories/`: Obtener lista de categorías.
*   `DELETE /books/{book_id}`: Eliminar un libro.
*   `DELETE /categories/{category_name}`: Eliminar una categoría y sus libros.
*   `GET /books/download/{book_id}`: Descargar un libro.
*   `POST /tools/convert-epub-to-pdf`: Convertir un EPUB a PDF.
*   `POST /rag/upload-book/`: Subir un libro para RAG.
*   `POST /rag/query/`: Consultar el sistema RAG.

