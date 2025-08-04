# Guía de Desarrollo

Esta sección proporciona una visión general de la arquitectura del proyecto y las convenciones de desarrollo para aquellos interesados en contribuir o entender mejor "Mi Librería Inteligente".

## Arquitectura del Proyecto

El proyecto se divide en dos componentes principales:

*   **Backend:** Una API RESTful construida con **FastAPI** (Python).
*   **Frontend:** Una aplicación de una sola página (SPA) desarrollada con **React** (JavaScript).

Ambos componentes se comunican a través de una API RESTful.

## Estructura de Directorios

```
/libreria
├── backend/
│   ├── alembic/             # Migraciones de base de datos
│   ├── crud.py              # Operaciones CRUD para la base de datos
│   ├── database.py          # Configuración de la base de datos (SQLAlchemy)
│   ├── main.py              # Puntos de entrada de la API FastAPI
│   ├── models.py            # Definiciones de modelos de SQLAlchemy
│   ├── rag.py               # Lógica para la función RAG (extracción, embeddings, ChromaDB, Gemini)
│   ├── requirements.txt     # Dependencias de Python
│   ├── schemas.py           # Esquemas de Pydantic para validación de datos
│   └── ...
├── frontend/
│   ├── public/              # Archivos estáticos (index.html, etc.)
│   ├── src/                 # Código fuente de React
│   │   ├── components/      # (Si se organizara así) Componentes reutilizables
│   │   ├── views/           # (Si se organizara así) Vistas principales (LibraryView, UploadView, etc.)
│   │   ├── App.js           # Componente principal de React y rutas
│   │   ├── Header.js        # Componente de navegación
│   │   ├── LibraryView.js   # Vista de la biblioteca de libros
│   │   ├── RagView.js       # Vista para la conversación con IA (RAG)
│   │   ├── ToolsView.js     # Vista para herramientas (conversor EPUB a PDF)
│   │   └── ...
│   ├── package.json         # Dependencias de Node.js y scripts
│   └── ...
├── .env.example             # Plantilla para variables de entorno
├── GEMINI.md                # Descripción general del proyecto
├── LICENSE                  # Información de licencia
├── README.md                # Descripción principal del proyecto
├── start.bat                # Script para iniciar ambos servidores (Windows)
├── stop.bat                 # Script para detener ambos servidores (Windows)
└── ...
```

## Convenciones de Desarrollo

### Backend (Python/FastAPI)

*   **SQLAlchemy:** Se utiliza para la interacción con la base de datos. Los modelos se definen en `models.py`.
*   **Alembic:** Para las migraciones de la base de datos.
*   **FastAPI:** Los puntos de entrada de la API se definen en `main.py`.
*   **Pydantic:** Se utiliza para la validación de datos de entrada y salida a través de `schemas.py`.
*   **Google Gemini API:** La interacción con Gemini se gestiona principalmente en `main.py` para el análisis inicial y en `rag.py` para la funcionalidad RAG.

### Frontend (React)

*   **Create React App:** El proyecto se inicializó con Create React App.
*   **React Router DOM:** Para la navegación entre vistas.
*   **Componentes:** Las vistas principales se encuentran en `src/` (ej. `LibraryView.js`, `UploadView.js`).
*   **Estilos:** Cada componente o vista tiene su propio archivo CSS (`.css`).

## Cómo Contribuir (Opcional)

Si estás interesado en contribuir al proyecto, por favor, sigue estos pasos:

1.  Haz un fork del repositorio.
2.  Crea una nueva rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3.  Realiza tus cambios y asegúrate de que el código cumpla con las convenciones existentes.
4.  Escribe pruebas si es aplicable.
5.  Envía un Pull Request detallando tus cambios.
