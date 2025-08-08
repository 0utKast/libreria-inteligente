import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [bookCount, setBookCount] = useState(0);

  useEffect(() => {
    const fetchBookCount = async () => {
      try {
        const response = await fetch('http://localhost:8001/books/count');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const count = await response.json();
        setBookCount(count);
      } catch (error) {
        console.error("Error fetching book count:", error);
      }
    };

    fetchBookCount();

    // Optional: Refetch count periodically or on specific events if needed
    const intervalId = setInterval(fetchBookCount, 30000); // Refetch every 30 seconds
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
