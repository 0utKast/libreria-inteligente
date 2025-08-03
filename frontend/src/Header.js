import React from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="app-header">
      <div className="header-logo">
        <h1>📚 Librería Inteligente</h1>
      </div>
      <nav className="header-nav">
        <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Mi Biblioteca
        </NavLink>
        <NavLink to="/upload" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Añadir Libro
        </NavLink>
        <NavLink to="/etiquetas" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Etiquetas
        </NavLink>
        <NavLink to="/herramientas" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Herramientas
        </NavLink>
        <NavLink to="/rag" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          Charla sobre libros con la IA
        </NavLink>
      </nav>
    </header>
  );
}

export default Header;
