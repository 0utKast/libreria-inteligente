import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [bookCount, setBookCount] = useState(0);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    const fetchBookCount = async () => {
      try {
        const response = await fetch('http://localhost:8001/books/count');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const count = await response.json();
        setBookCount(count);
        setErrorMessage(null); // Clear any previous error
      } catch (error) {
        console.error("Error fetching book count:", error);
        setErrorMessage("Error al cargar el contador de libros.");
        setBookCount(0); // Clear book count on error
      }
    };

    fetchBookCount();

    // Refetch count periodically (every 5 minutes)
    const intervalId = setInterval(fetchBookCount, 300000);
    return () => clearInterval(intervalId);
  }, []);

  const handleLinkClick = () => {
    setMenuOpen(false);
  };

  return (
    <header className="app-header">
      <div className="header-logo">
        <h1>📚 Librería Inteligente</h1>
        {bookCount > 0 && (
          <p className="book-count">{bookCount} libros en la biblioteca</p>
        )}
        {errorMessage && (
          <p className="error-message">{errorMessage}</p>
        )}
      </div>
      <button className="hamburger-menu" onClick={() => setMenuOpen(!menuOpen)}>
        &#9776;
      </button>
      <nav className={`header-nav ${menuOpen ? 'open' : ''}`}>
        <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={handleLinkClick}>
          Mi Biblioteca
        </NavLink>
        <NavLink to="/upload" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={handleLinkClick}>
          Añadir Libro
        </NavLink>
        <NavLink to="/etiquetas" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={handleLinkClick}>
          Etiquetas
        </NavLink>
        <NavLink to="/herramientas" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={handleLinkClick}>
          Herramientas
        </NavLink>
        <NavLink to="/rag" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} onClick={handleLinkClick}>
          Charla sobre libros con la IA
        </NavLink>
      </nav>
    </header>
  );
}

export default Header;
