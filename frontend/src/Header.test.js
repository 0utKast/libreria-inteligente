import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './Header';
import { BrowserRouter as Router } from 'react-router-dom';

jest.mock('./config', () => ({ API_URL: '/api' }));

const mockFetch = jest.fn();
global.fetch = mockFetch;


describe('Header Component', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders the header correctly', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(5),
    });
    render(<Router><Header /></Router>);
    expect(screen.getByRole('heading', { name: /📚 Librería Inteligente/i })).toBeInTheDocument();
    expect(await screen.findByText('5 libros en la biblioteca')).toBeInTheDocument();
  });


  it('handles error during fetch', async () => {
    mockFetch.mockRejectedValue(new Error('Failed to fetch'));
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/No se pudo cargar el contador de libros/i)).toBeInTheDocument();
    expect(screen.queryByText(/libros en la biblioteca/i)).not.toBeInTheDocument();
  });


  it('toggles the menu on hamburger click', () => {
    render(<Router><Header /></Router>);
    const hamburgerButton = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);

  });

  it('closes the menu on link click', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(10),
    });
    render(<Router><Header /></Router>);
    const hamburgerButton = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
    const link = screen.getByRole('link', { name: /Mi Biblioteca/i });
    fireEvent.click(link);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);
  });

  it('renders nav links correctly', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(10),
    });
    render(<Router><Header /></Router>);
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Añadir Libro/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Etiquetas/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Herramientas/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Charla sobre libros con la IA/i })).toBeInTheDocument();
  });

  it('shows error message if fetch fails', async () => {
    mockFetch.mockRejectedValue(new Error('Failed to fetch'));
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/No se pudo cargar el contador de libros/i)).toBeInTheDocument();
  });

  it('shows zero books if fetch fails', async () => {
      mockFetch.mockRejectedValue(new Error('Failed to fetch'));
      render(<Router><Header /></Router>);
      expect(await screen.findByText(/No se pudo cargar el contador de libros/i)).toBeInTheDocument();
      expect(screen.queryByText(/libros en la biblioteca/i)).not.toBeInTheDocument();
  });

  it('does not show book count if bookCount is 0 and no error', async () => {
      mockFetch.mockResolvedValue({
          ok: true,
          json: () => Promise.resolve(0),
      });
      render(<Router><Header /></Router>);
      expect(screen.queryByText(/libros en la biblioteca/i)).not.toBeInTheDocument();
  });

});
```