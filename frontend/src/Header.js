import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLinkClick = () => {
    setMenuOpen(false);
  };

  return (
    <header className="app-header">
      <div className="header-logo">
        <h1>📚 Librería Inteligente</h1>
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
