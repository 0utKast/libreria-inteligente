
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
