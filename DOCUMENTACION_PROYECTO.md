# DOCUMENTACION_PROYECTO.md

## 1. Descripción General del Proyecto

"Mi Librería Inteligente" es una aplicación web completa para gestionar una colección de libros digitalmente. Permite a los usuarios subir libros en formato PDF y EPUB, los cuales son analizados por una IA para extraer metadatos (título, autor, categoría).  La aplicación ofrece una interfaz para buscar, visualizar y descargar los libros, además de una herramienta para convertir EPUB a PDF.  También incluye una funcionalidad de Recuperación de la Información basada en Preguntas y Respuestas (RAG) para interactuar con el contenido de los libros a través de una interfaz de chat.

La arquitectura de la aplicación se basa en tres componentes principales:

* **Frontend:** Desarrollado con React.js, proporciona una interfaz de usuario intuitiva para interactuar con la aplicación.
* **Backend:** Desarrollado con FastAPI, un framework Python para APIs. Se encarga de procesar las solicitudes del frontend, gestionar la base de datos y la lógica de negocio, incluyendo la integración con la IA.
* **Base de Datos:** Se utiliza una base de datos SQLite para almacenar la información de los libros.

## 2. Estructura del Proyecto

El proyecto se estructura de la siguiente manera:

* `backend/`: Contiene el código del backend de Python/FastAPI.
    * `alembic/`:  Contiene las migraciones de la base de datos.
    * `schemas.py`: Define los modelos Pydantic para la serialización y validación de datos.
    * `crud.py`: Implementa las operaciones CRUD (Create, Read, Update, Delete) para la base de datos.
    * `database.py`: Configura la conexión a la base de datos SQLite.
    * `models.py`: Define los modelos SQLAlchemy para la base de datos.
    * `main.py`:  El archivo principal del backend, define las rutas de la API.
    * `rag.py`: Implementa la lógica para el sistema RAG (Retrieval Augmented Generation).
* `frontend/`: Contiene el código del frontend React.js.
    * `src/`: Contiene el código fuente del frontend.
        * `components/`:  (Implícito) Contiene componentes React.
        * `config.js`: Define la URL base de la API.
        * `App.js`: Componente principal de la aplicación.
        * `Header.js`: Componente de encabezado.
        * `LibraryView.js`: Componente para visualizar la biblioteca.
        * `UploadView.js`: Componente para subir libros.
        * `CategoriesView.js`: Componente para mostrar las categorías.
        * `ToolsView.js`: Componente para las herramientas de conversión de archivos.
        * `ReaderView.js`: Componente para leer los libros EPUB.
        * `RagView.js`: Componente para la interfaz de chat con RAG.
    * `public/`: (Implícito) Contiene archivos estáticos.

## 3. Análisis Detallado del Backend (Python/FastAPI)

### `backend/schemas.py`

* **Propósito:** Define los modelos Pydantic para la serialización y validación de datos.

```python
class BookBase(BaseModel):
    title: str
    author: str
    category: str
    cover_image_url: str | None = None
    file_path: str

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True

class ConversionResponse(BaseModel):
    download_url: str

class RagUploadResponse(BaseModel):
    book_id: str
    message: str

class RagQuery(BaseModel):
    query: str
    book_id: str

class RagQueryResponse(BaseModel):
    response: str
```

### `backend/crud.py`

* **Propósito:** Implementa las operaciones CRUD para la base de datos.

```python
# ... (código de la función crud.py) ...
```

### `backend/database.py`

* **Propósito:** Configura la conexión a la base de datos SQLite.

```python
# ... (código de la función database.py) ...
```

### `backend/models.py`

* **Propósito:** Define los modelos SQLAlchemy para la base de datos.

```python
# ... (código de la función models.py) ...
```

### `backend/rag.py`

* **Propósito:** Implementa la lógica para el sistema RAG.

```python
# ... (código de la función rag.py) ...
```

### `backend/main.py`

* **Propósito:** El archivo principal del backend, define las rutas de la API.

```python
# ... (código de la función main.py) ...
```


## 4. Análisis Detallado del Frontend (React)

### `frontend/src/App.js`

* **Propósito:** Componente principal de la aplicación, gestiona las rutas.
* **Estado:** No tiene estado propio.
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** No tiene efectos secundarios.

### `frontend/src/Header.js`

* **Propósito:** Componente de encabezado de la aplicación, con menú de navegación.
* **Estado:** `menuOpen` (booleano), `bookCount` (entero), `errorMessage` (string).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** Realiza una petición al backend para obtener el número total de libros, actualiza periodicamente.
* **Interacción con Backend:**  Realiza una petición GET a `/books/count`.

### `frontend/src/LibraryView.js`

* **Propósito:**  Visualiza la lista de libros de la biblioteca.
* **Estado:** `books` (array), `searchTerm` (string), `error` (string), `loading` (booleano), `isMobile` (booleano).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** Realiza una petición al backend para obtener los libros, con debounce para la búsqueda.
* **Interacción con Backend:** Realiza peticiones GET a `/books/` con parámetros de búsqueda o filtro.

### `frontend/src/UploadView.js`

* **Propósito:** Permite a los usuarios subir libros.
* **Estado:** `filesToUpload` (array), `isUploading` (booleano).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** No tiene efectos secundarios.
* **Interacción con Backend:** Realiza peticiones POST a `/upload-book/` para cada libro subido.

### `frontend/src/ToolsView.js`

* **Propósito:** Contiene herramientas para la gestión de libros, actualmente solo el convertidor EPUB a PDF.
* **Estado:** (Dentro de `EpubToPdfConverter`) `selectedFile` (objeto File), `message` (string), `isLoading` (booleano).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** No tiene efectos secundarios.
* **Interacción con Backend:** Realiza una petición POST a `/tools/convert-epub-to-pdf` para la conversión.

### `frontend/src/ReaderView.js`

* **Propósito:** Visualiza un libro EPUB usando ReactReader.
* **Estado:** `location` (string), `epubData` (arrayBuffer), `isLoading` (booleano), `error` (string).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** Realiza una petición para descargar el libro.
* **Interacción con Backend:** Realiza una petición GET a `/books/download/{bookId}`.

### `frontend/src/RagView.js`

* **Propósito:** Permite al usuario interactuar con la IA usando el modelo RAG.
* **Estado:** `selectedFile` (objeto File), `message` (string), `isLoading` (booleano), `bookId` (string), `chatHistory` (array), `currentQuery` (string).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:** No tiene efectos secundarios.
* **Interacción con Backend:**  Realiza peticiones POST a `/rag/upload-book/` y `/rag/query/`.

### `frontend/src/CategoriesView.js`

* **Propósito:**  Muestra la lista de categorías disponibles.
* **Estado:** `categories` (array), `error` (string), `loading` (booleano).
* **Propiedades:** No tiene propiedades.
* **Efectos Secundarios:**  Obtiene las categorías del backend.
* **Interacción con Backend:** Realiza una petición GET a `/categories/`.


## 5. Flujo de Datos y API

1.  **Subida de libro:** El usuario selecciona un archivo (PDF o EPUB) en `UploadView.js`.
2.  **Envío al backend:** El frontend envía el archivo al endpoint `/upload-book/` (POST).
3.  **Procesamiento en el backend:** `main.py` recibe el archivo, lo procesa (`process_pdf` o `process_epub`), lo analiza con Gemini (`analyze_with_gemini`), extrae los metadatos y guarda el libro en el sistema de archivos y la base de datos usando `crud.create_book`.
4.  **Almacenamiento:** La información del libro se guarda en la base de datos (tabla `books` en `models.py`).
5.  **Visualización:** `LibraryView.js` obtiene la lista de libros de `/books/` (GET) y los muestra.  Los libros se pueden buscar a través de `/books/search/` (GET). Las categorías se obtienen mediante `/categories/` (GET).
6.  **Descarga de libro:** El usuario puede descargar un libro desde `/books/download/{book_id}` (GET).
7.  **Conversión EPUB a PDF:** El usuario sube un archivo EPUB a `/tools/convert-epub-to-pdf` (POST), el backend lo procesa y devuelve la URL de descarga del PDF.
8. **RAG:** El usuario sube un libro para RAG en `/rag/upload-book/` (POST), se procesa y se indexa para generar embeddings. El usuario puede consultar a través de `/rag/query/` (POST).

**Endpoints de la API:**

* `/upload-book/` (POST): Sube un libro.
* `/books/` (GET): Obtiene una lista de libros (con opciones de filtrado).
* `/books/count` (GET): Obtiene el número total de libros.
* `/books/search/` (GET): Busca libros por título parcial.
* `/categories/` (GET): Obtiene una lista de categorías.
* `/books/{book_id}` (DELETE): Elimina un libro.
* `/categories/{category_name}` (DELETE): Elimina una categoría y sus libros.
* `/books/download/{book_id}` (GET): Descarga un libro.
* `/tools/convert-epub-to-pdf` (POST): Convierte un EPUB a PDF.
* `/rag/upload-book/` (POST): Sube un libro para RAG.
* `/rag/query/` (POST): Realiza una consulta RAG.