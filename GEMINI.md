
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
**Workflow File:** `.github/workflows/auto-test.yml`
**Trigger:** `pull_request` to `main` branch.
**Mechanism:**
1.  Detects modified `.py` or `.js` files in the PR.
2.  Sends file content to Gemini API with a prompt to generate unit tests.
3.  Creates new test files (e.g., `backend/tests/test_*.py`, `frontend/src/*.test.js`).
4.  Commits these new test files back to the PR branch for review.

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

### Automated Unit Test Execution

**Suggestion:** Implement a GitHub Action to automatically run all unit tests (both backend Python tests and frontend JavaScript tests) on every Pull Request.
**Benefit:** Provides immediate feedback on code quality and prevents merging code that breaks existing tests.
**Considerations:**
*   Requires setting up Python and Node.js environments.
*   Running `pytest` for backend tests.
*   Running `npm test` for frontend tests.
*   Reporting test results back to the Pull Request status checks.
