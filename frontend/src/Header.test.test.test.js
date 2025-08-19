import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './Header';
import { BrowserRouter as Router } from 'react-router-dom';

jest.mock('./config', () => ({
  default: 'http://test-api'
}));

jest.mock('node-fetch', () => jest.fn());
const fetch = require('node-fetch');


describe('Header Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders header with initial state', async () => {
    fetch.mockResolvedValueOnce({ ok: true, json: async () => 10 });
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/📚 Librería Inteligente/i)).toBeInTheDocument();
    expect(screen.getByText(/10 libros en la biblioteca/i)).toBeInTheDocument();
  });


  test('renders error message if fetch fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed to fetch'));
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/No se pudo cargar el contador de libros/i)).toBeInTheDocument();
    expect(screen.queryByText(/10 libros en la biblioteca/i)).not.toBeInTheDocument();
  });

  test('toggles menu on hamburger click', () => {
    render(<Router><Header /></Router>);
    const hamburgerButton = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);
  });

  test('closes menu on link click', () => {
    render(<Router><Header /></Router>);
    const hamburgerButton = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
    const navLink = screen.getByRole('link', { name: /Mi Biblioteca/i });
    fireEvent.click(navLink);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);
  });

  test('nav links render correctly', () => {
    render(<Router><Header /></Router>);
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Añadir Libro/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Etiquetas/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Herramientas/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Charla sobre libros con la IA/i })).toBeInTheDocument();
  });

  test('updates book count after fetch', async () => {
    fetch.mockResolvedValueOnce({ ok: true, json: async () => 15 });
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/15 libros en la biblioteca/i)).toBeInTheDocument();
  });

  test('handles fetch error gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed to fetch'));
    render(<Router><Header /></Router>);
    await screen.findByText(/No se pudo cargar el contador de libros/i);
  });

  test('renders correctly with no books', async () => {
    fetch.mockResolvedValueOnce({ ok: true, json: async () => 0 });
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/0 libros en la biblioteca/i)).toBeInTheDocument();
  });

  test('renders correctly with a large number of books', async () => {
    fetch.mockResolvedValueOnce({ ok: true, json: async () => 1000 });
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/1000 libros en la biblioteca/i)).toBeInTheDocument();
  });


  test('shows loading indicator while fetching', async () => {
    fetch.mockImplementation(() => new Promise(resolve => setTimeout(() => resolve({ok: true, json: async () => 10}), 500)));
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/Cargando.../i)).toBeInTheDocument();
    expect(await screen.findByText(/10 libros en la biblioteca/i)).toBeInTheDocument();
  });

  test('handles network error', async () => {
    fetch.mockRejectedValueOnce({ok:false, status: 500});
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/Error de red al cargar el contador de libros/i)).toBeInTheDocument();
  })

  test('handles invalid JSON response', async () => {
    fetch.mockResolvedValueOnce({ ok: true, json: async () => { throw new Error("Invalid JSON"); } });
    render(<Router><Header /></Router>);
    expect(await screen.findByText(/Error al procesar la respuesta del servidor/i)).toBeInTheDocument();
  })
});
```