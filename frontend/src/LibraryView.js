import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import './LibraryView.css';

// Hook personalizado para debounce
const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  return debouncedValue;
};

// Componente para la portada (con fallback a genérica)
const BookCover = ({ src, alt, title }) => {
  const [hasError, setHasError] = useState(false);
  useEffect(() => { setHasError(false); }, [src]);
  const handleError = () => { setHasError(true); };

  if (hasError || !src) {
    const initial = title ? title[0].toUpperCase() : '?';
    return (
      <div className="generic-cover">
        <span className="generic-cover-initial">{initial}</span>
      </div>
    );
  }
  return <img src={src} alt={alt} className="book-cover" onError={handleError} />;
};

function LibraryView() {
  const [books, setBooks] = useState([]);
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 300);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  const handleAuthorClick = (author) => {
    setSearchTerm(''); // Clear general search term
    setSearchParams({ author: author }); // Use 'author' parameter
  };

  const handleCategoryClick = (category) => {
    setSearchParams({ category: category });
  };

  const fetchBooks = useCallback(async () => {
    setLoading(true);
    setError('');
    
    const params = new URLSearchParams();
    const category = searchParams.get('category');
    const author = searchParams.get('author'); // Get the new 'author' parameter

    if (category) {
      params.append('category', category);
    }
    if (author) {
      params.append('author', author); // Append 'author' to params
    } else if (debouncedSearchTerm) {
      params.append('search', debouncedSearchTerm);
    }

    const url = `http://localhost:8001/books/?${params.toString()}`;
    
    try {
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setBooks(data);
      } else {
        setError('No se pudieron cargar los libros.');
      }
    } catch (err) {
      setError('Error de conexión al cargar la biblioteca.');
    } finally {
      setLoading(false);
    }
  }, [debouncedSearchTerm, searchParams]);

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  const handleDeleteBook = async (bookId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este libro?')) {
      try {
        const response = await fetch(`http://localhost:8001/books/${bookId}`, { method: 'DELETE' });
        if (response.ok) {
          setBooks(prevBooks => prevBooks.filter(b => b.id !== bookId));
        } else {
          alert('No se pudo eliminar el libro.');
        }
      } catch (err) {
        alert('Error de conexión al intentar eliminar el libro.');
      }
    }
  };

  return (
    <div className="library-container">
      <h2>Mi Biblioteca</h2>
      
      <div className="controls-container">
        <input
          type="text"
          placeholder="Buscar por título, autor o categoría..."
          className="search-bar"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {error && <p className="error-message">{error}</p>}
      {loading && <p>Cargando libros...</p>}
      {!loading && books.length === 0 && !error && <p>No se encontraron libros que coincidan con tu búsqueda.</p>}

      <div className="book-grid">
        {books.map((book) => (
          <div key={book.id} className="book-card">
            <button onClick={() => handleDeleteBook(book.id)} className="delete-book-btn" title="Eliminar libro">×</button>
            <BookCover 
              src={book.cover_image_url ? `http://localhost:8001/${book.cover_image_url}` : ''}
              alt={`Portada de ${book.title}`}
              title={book.title}
            />
            <div className="book-card-info">
              <h3>{book.title}</h3>
              <p className="clickable-text" onClick={() => handleAuthorClick(book.author)}>{book.author}</p>
              <span className="clickable-text" onClick={() => handleCategoryClick(book.category)}>{book.category}</span>
            </div>
            {book.file_path.toLowerCase().endsWith('.pdf') ? (
              <a 
                href={`http://localhost:8001/books/download/${book.id}`} 
                className="download-button" 
                target="_blank" 
                rel="noopener noreferrer"
              >
                Abrir PDF
              </a>
            ) : (
              <Link to={`/leer/${book.id}`} className="download-button">
                Leer EPUB
              </Link>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default LibraryView;
