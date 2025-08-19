import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './Header';
import { BrowserRouter as Router } from 'react-router-dom';

jest.mock('./config', () => ({ default: 'http://test-api' }));

describe('Header Component', () => {
  const mockFetch = jest.fn();
  global.fetch = mockFetch;

  beforeEach(() => {
    mockFetch.mockClear();
  });

  it('renders without crashing', () => {
    render(<Router><Header /></Router>);
  });

  it('displays the correct header title', () => {
    render(<Router><Header /></Router>);
    expect(screen.getByRole('heading', { name: /📚 Librería Inteligente/i })).toBeInTheDocument();
  });

  it('displays initial book count and updates it after successful fetch', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => 10,
    });
    render(<Router><Header /></Router>);
    expect(await screen.findByText('10 libros en la biblioteca')).toBeInTheDocument();
  });

  it('displays an error message after failed fetch', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Failed to fetch'));
    render(<Router><Header /></Router>);
    expect(await screen.findByText('No se pudo cargar el contador de libros. Inténtalo de nuevo más tarde.')).toBeInTheDocument();
    expect(screen.queryByText(/libros en la biblioteca/i)).not.toBeInTheDocument();
  });


  it('toggles menu on hamburger click', () => {
    render(<Router><Header /></Router>);
    const hamburgerButton = screen.getByRole('button', {name: /&#9776;/i});
    fireEvent.click(hamburgerButton);
    expect(screen.getByTestId('header-nav')).toHaveClass('open');
    fireEvent.click(hamburgerButton);
    expect(screen.getByTestId('header-nav')).not.toHaveClass('open');
  });


  it('closes menu on link click', () => {
    render(<Router><Header /></Router>);
    const hamburgerButton = screen.getByRole('button', {name: /&#9776;/i});
    fireEvent.click(hamburgerButton);
    expect(screen.getByTestId('header-nav')).toHaveClass('open');
    fireEvent.click(screen.getByRole('link', { name: /Mi Biblioteca/i }));
    expect(screen.getByTestId('header-nav')).not.toHaveClass('open');
  });

  it('renders nav links correctly', () => {
    render(<Router><Header /></Router>);
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Añadir Libro/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Etiquetas/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Herramientas/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Charla sobre libros con la IA/i })).toBeInTheDocument();
  });

});