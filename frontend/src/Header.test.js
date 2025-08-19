import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './Header';
import { BrowserRouter } from 'react-router-dom';

jest.mock('./config', () => ({ default: 'http://test-api' }));

describe('Header Component', () => {
  const mockFetch = jest.spyOn(window, 'fetch');

  beforeEach(() => {
    mockFetch.mockImplementation(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ count: 10 }),
      })
    );
  });

  afterEach(() => {
    mockFetch.mockClear();
  });


  it('renders the header with initial state', async () => {
    render(<BrowserRouter><Header /></BrowserRouter>);
    expect(screen.getByText(/📚 Librería Inteligente/i)).toBeInTheDocument();
    expect(screen.getByText(/10 libros en la biblioteca/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /&#9776;/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i })).toBeInTheDocument();

  });

  it('toggles the menu on hamburger click', async () => {
    render(<BrowserRouter><Header /></BrowserRouter>);
    const button = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(button);
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i })).toHaveClass('nav-link');
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i }).closest('nav')).toHaveClass('open');
    fireEvent.click(button);
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i }).closest('nav')).not.toHaveClass('open');
  });


  it('handles link clicks and closes the menu', async () => {
    render(<BrowserRouter><Header /></BrowserRouter>);
    const button = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(button);
    const link = screen.getByRole('link', { name: /Mi Biblioteca/i });
    fireEvent.click(link);
    expect(screen.getByRole('link', { name: /Mi Biblioteca/i }).closest('nav')).not.toHaveClass('open');

  });

  it('displays error message on fetch failure', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Failed to fetch'));
    render(<BrowserRouter><Header /></BrowserRouter>);
    await screen.findByText(/No se pudo cargar el contador de libros/i);
  });

  it('shows zero books if fetch fails', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Failed to fetch'));
    render(<BrowserRouter><Header /></BrowserRouter>);
    await screen.findByText(/0 libros en la biblioteca/i);

  });

  it('displays correct number of books', async () => {
    mockFetch.mockImplementation(() => 
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ count: 25 }),
      })
    );
    render(<BrowserRouter><Header /></BrowserRouter>);
    expect(await screen.findByText(/25 libros en la biblioteca/i)).toBeInTheDocument();
  });

});