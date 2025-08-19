# GEMINI.md

## Project Overview

This project is a full-stack web application called "Mi Librería Inteligente" (My Smart Library). It allows users to upload and manage a digital book collection (PDF and EPUB files). The application uses the Google Gemini AI to automatically analyze the books, extract metadata like title, author, and category, and even find the book's cover image.

The project is divided into two main parts:

*   **Backend:** A Python-based API built with the FastAPI framework. It handles file uploads, processing, interaction with the Gemini API, and database operations.
*   **Frontend:** A JavaScript-based single-page application (SPA) built with React. It provides the user interface for uploading, viewing, and managing the book library.

### Key Technologies

*   **Backend:** Python, FastAPI, SQLAlchemy, Alembic, Google Gemini Pro, PyMuPDF, EbookLib
*   **Frontend:** React, React Router
*   **Database:** SQLite

## Automated GitHub Actions

This project leverages GitHub Actions and the Google Gemini API to automate various software engineering tasks.

### Automated Unit Test Generation

**Purpose:** Automatically generates basic unit tests for modified Python (`pytest`) and JavaScript (`Jest`) files in a Pull Request.
**Workflow File:** `.github/workflows/ci.yml` (previously `auto-test.yml`)
**Trigger:** `pull_request` to `main` branch.
**Mechanism:**
1.  Detects modified `.py` or `.js` files in the PR.
2.  Sends file content to Gemini API with a prompt to generate unit tests.
3.  Creates new test files (e.g., `backend/tests/test_*.py`, `frontend/src/*.test.js`).
4.  Commits these new test files back to the PR branch for review.

### Automated Unit Test Execution

**Purpose:** Automatically runs all unit tests (both backend Python tests and frontend JavaScript tests) on every Pull Request.
**Workflow File:** `.github/workflows/ci.yml` (previously `run-tests.yml`)
**Trigger:** `pull_request` to `main` branch.
**Mechanism:**
1.  Sets up Python and Node.js environments.
2.  Installs dependencies for both backend and frontend.
3.  Runs `pytest` for backend tests.
4.  Runs `npm test` for frontend tests.
5.  Reports test results back to the Pull Request status checks.

**Current Issue with `run-tests` job (within `ci.yml`):**

The `run-tests` job is currently failing. The main issues observed are:

1.  **`Exception: No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.`**: This error occurs because the `GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variable is not being correctly passed to the `test` job's environment in GitHub Actions. This is crucial for the `rag.py` module, which relies on the Gemini API.
2.  **`sqlalchemy.exc.InvalidRequestError: Table 'books' is already defined for this MetaData instance.`**: This error suggests that the SQLAlchemy `Book` model is being defined multiple times during test collection, likely due to how `pytest` discovers and imports test modules. This can be mitigated by using `extend_existing=True` in the model definition, but a more robust solution might involve better test isolation or fixtures.
3.  **`SyntaxError: invalid syntax`**: This error persists in some generated test files, indicating that the `generate_tests.py` script's logic for removing markdown code fences (```) is not entirely robust, or that the Gemini API's output sometimes includes unexpected characters or formatting that the current regex doesn't handle.
4.  **Increased Execution Time for `generate-tests`**: The `generate-tests` job is taking an increasingly long time to execute (currently over 8 minutes). This is likely due to the continuous generation and accumulation of new test files, which are then processed in subsequent runs, creating a feedback loop.

**Latest Error Log from `errores.txt`:**

```
Run export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
============================= test session starts ==============================
platform linux -- Python 3.11.13, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/runner/work/libreria-inteligente/libreria-inteligente
plugins: anyio-4.10.0
collected 56 items / 16 errors

==================================== ERRORS ====================================
_________________ ERROR collecting backend/tests/test_main.py __________________
backend/tests/test_main.py:5: in <module>
    from backend.main import (
backend/main.py:19: in <module>
    import rag # Import the new RAG module
    ^^^^^^^^^^
backend/rag.py:15: in <module>
    raise Exception("No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.")
E   Exception: No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.
________________ ERROR collecting backend/tests/test_models.py _________________
.venv/lib/python3.11/site-packages/_pytest/python.py:498: in importtestmodule
    mod = import_path(
.venv/lib/python3.11/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1204: in _gcd_import
    ???
<frozen importlib._bootstrap>:1176: in _find_and_load
    ???
<frozen importlib._bootstrap>:1147: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:690: in _load_unlocked
    ???
.venv/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:177: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.11/site-packages/_pytest/assertion/rewrite.py:357: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
ERROR backend/tests/test_models.py
ERROR backend/tests/test_test_main.py - Exception: No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.
ERROR backend/tests/test_test_models.py - sqlalchemy.exc.InvalidRequestError: Table 'books' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
ERROR backend/tests/test_test_test_main.py - Exception: No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.
ERROR backend/tests/test_test_test_models.py - sqlalchemy.exc.InvalidRequestError: Table 'books' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
ERROR backend/tests/test_test_test_test_main.py - Exception: No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.
ERROR backend/tests/test_test_test_test_models.py - sqlalchemy.exc.InvalidRequestError: Table 'books' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
ERROR backend/tests/test_test_test_test_test_main.py - Exception: No se encontró la variable de entorno GOOGLE_API_KEY ni GEMINI_API_KEY.
ERROR backend/tests/test_test_test_test_test_models.py - sqlalchemy.exc.InvalidRequestError: Table 'books' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
ERROR backend/tests/test_test_test_test_test_test_models.py - sqlalchemy.exc.InvalidRequestError: Table 'books' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
ERROR backend/tests/test_test_test_test_test_utils.py
ERROR backend/tests/test_test_test_test_utils.py
ERROR backend/tests/test_test_test_utils.py
ERROR backend/tests/test_test_utils.py
ERROR backend/tests/test_utils.py
!!!!!!!!!!!!!!!!!!! Interrupted: 16 errors during collection !!!!!!!!!!!!!!!!!!!
======================= 10 warnings, 16 errors in 4.87s ========================
sys:1: DeprecationWarning: builtin type swigvarlink has no __module__ attribute
Error: Process completed with exit code 2.
```

## Building and Running

### Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    # source .venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the initial database:**
    ```bash
    alembic upgrade head
    ```

5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload --port 8001
    ```

### Frontend

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm start
    ```

The application will be available at `http://localhost:3000`.

## Development Conventions

*   **Backend:** The backend code follows a standard FastAPI project structure. It uses SQLAlchemy for database interactions and Alembic for database migrations. The main application logic is in `main.py`, with database models, schemas, and CRUD operations separated into their respective files.
*   **Frontend:** The frontend is a typical React application created with `create-react-app`. It uses React Router for navigation and has separate components for each view.
*   **API:** The frontend and backend communicate via a RESTful API. The API endpoints are defined in the backend's `main.py` file.

## Future Improvements / Suggestions from Gemini Review

Based on the recent Pull Request review, here are some suggestions for future improvements:

### Backend

*   **Security - CORS Configuration:** The current `allow_origins=["http://localhost:3000"]` in `main.py` is restrictive. For production environments, consider replacing it with the actual frontend origin or using an environment variable for flexibility.
*   **Error Handling:** Implement more specific error handling in `main.py` for different file types (PDF, EPUB) during processing.
*   **Testing:** Add unit tests for new functions and API endpoints to ensure code quality and reliability.
*   **Consistency:** Ensure consistent use of `async/await` throughout the asynchronous code.
*   **Documentation:** Add comprehensive documentation for new API endpoints.

### Frontend

*   **Performance - Book Count Refetch:** The book count refetch interval in `Header.js` (currently every minute) might be excessive. Consider a longer interval or activating it only when necessary.
*   **Usability - Error Messages:** Make error messages in `Header.js` more informative for the user.
*   **Error Handling:** Implement retry mechanisms or better error state handling for the book count fetching logic in `Header.js`.