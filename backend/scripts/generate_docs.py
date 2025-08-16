import os
import google.generativeai as genai
import pathlib

# --- Configuration ---
# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=GEMINI_API_KEY)

# --- File Discovery ---
# Define project root and paths to scan
project_root = pathlib.Path(__file__).parent.parent.parent
backend_path = project_root / "backend"
frontend_path = project_root / "frontend" / "src"
output_file_path = project_root / "DOCUMENTACION_PROYECTO.md"

# Globs for file types to include
backend_files_glob = "**/*.py"
frontend_files_glob = "**/*.js"

# Paths/files to exclude
exclude_patterns = [
    "**/node_modules/**",
    "**/.venv/**",
    "**/__pycache__/**",
    "**/*test.js",
    "**/setupTests.js",
    "**/reportWebVitals.js",
    "**/alembic/**",
    "**/scripts/**",
]

def find_files(start_path, glob_pattern, excludes):
    """Finds files matching a glob pattern, excluding specified paths."""
    files_found = []
    # Use rglob for recursive search
    for path in pathlib.Path(start_path).rglob(glob_pattern):
        # Check if the path is within any of the exclude patterns
        if not any(path.match(p) for p in excludes):
            files_found.append(path)
    return files_found

# --- Content Aggregation ---
def read_file_content(file_path):
    """Reads the content of a file and returns it with a header."""
    try:
        # Ensure we are using the project root to create the relative path
        relative_path = file_path.relative_to(project_root)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"--- Contenido del archivo: {relative_path} ---\n\n```\n{content}\n```\n\n"
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")
        return ""

# --- Prompt Generation ---
def create_prompt(all_files_content):
    """Creates the final prompt for the Gemini API."""
    return f'''
Eres un ingeniero de software senior y escritor técnico encargado de crear la documentación para un nuevo proyecto.

A continuación se muestra el contenido completo de todos los archivos de código fuente relevantes del proyecto "Mi Librería Inteligente".

{all_files_content}

Tu tarea es generar un archivo Markdown de alta calidad (`DOCUMENTACION_PROYECTO.md`) que sirva como la documentación técnica principal del proyecto.

El documento debe estar bien estructurado y ser fácil de navegar. Sigue esta estructura:

1.  **Descripción General del Proyecto:**
    *   Un resumen de alto nivel de lo que hace la aplicación "Mi Librería Inteligente".
    *   Describe la arquitectura general (frontend de React, backend de FastAPI, base de datos, etc.).

2.  **Estructura del Proyecto:**
    *   Proporciona un resumen de la estructura de directorios, explicando el propósito de las carpetas clave (`backend/`, `frontend/src`, etc.).

3.  **Análisis Detallado del Backend (Python/FastAPI):**
    *   Para cada archivo `.py` importante (`main.py`, `crud.py`, `models.py`, `rag.py`, etc.):
        *   Describe el propósito principal del archivo.
        *   Documenta cada función o clase principal, explicando su lógica, parámetros y valores de retorno. Utiliza un formato claro.

4.  **Análisis Detallado del Frontend (React):**
    *   Para cada componente `.js` importante (`App.js`, `LibraryView.js`, `UploadView.js`, etc.):
        *   Describe el propósito del componente.
        *   Explica su estado (state), propiedades (props) y los principales efectos secundarios (effects).
        *   Describe las interacciones del usuario y cómo se comunica con el backend.

5.  **Flujo de Datos y API:**
    *   Describe cómo fluyen los datos a través de la aplicación, desde la carga de un libro en el frontend hasta su procesamiento y almacenamiento en el backend.
    *   Resume los principales endpoints de la API definidos en el backend.

Genera únicamente el contenido del archivo Markdown. No incluyas ninguna otra explicación o texto introductorio fuera del propio documento.
'''

# --- Main Execution ---
if __name__ == "__main__":
    print("Iniciando la generación de documentación...")

    # Find all relevant files
    backend_files = find_files(backend_path, backend_files_glob, exclude_patterns)
    frontend_files = find_files(frontend_path, frontend_files_glob, exclude_patterns)
    all_files = backend_files + frontend_files

    print(f"Archivos encontrados: {len(all_files)}")
    # for file in all_files:
    #     print(f"  - {file.relative_to(project_root)}")


    # Read content from all files
    aggregated_content = "".join([read_file_content(f) for f in all_files])

    if not aggregated_content:
        print("No se encontró contenido para documentar. Saliendo.")
        exit()

    # Create the prompt
    prompt = create_prompt(aggregated_content)
    print("Prompt generado. Enviando a la API de Gemini...")

    # Call the Gemini API
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

    print("Respuesta recibida de Gemini. Escribiendo en el archivo de documentación...")
    # Write the response to the output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Documentación generada exitosamente en {output_file_path}")
