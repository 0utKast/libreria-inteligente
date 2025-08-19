import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './Header';
import { BrowserRouter as Router } from 'react-router-dom';

jest.mock('./config', () => ({ default: 'http://test-api' }));

const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('Header Component', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });


  test('renders header component', () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => 10,
    });
    render(
      <Router>
        <Header />
      </Router>
    );
    expect(screen.getByText('📚 Librería Inteligente')).toBeInTheDocument();
  });

  test('displays book count', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => 15,
    });
    render(
      <Router>
        <Header />
      </Router>
    );
    expect(await screen.findByText('15 libros en la biblioteca')).toBeInTheDocument();
  });

  test('displays error message on fetch failure', async () => {
    mockFetch.mockRejectedValue(new Error('Failed to fetch'));
    render(
      <Router>
        <Header />
      </Router>
    );
    expect(await screen.findByText('No se pudo cargar el contador de libros. Inténtalo de nuevo más tarde.')).toBeInTheDocument();
  });

  test('toggles menu on hamburger click', () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    const button = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(button);
    expect(screen.getByText('Mi Biblioteca')).toBeVisible();
    fireEvent.click(button);
    expect(screen.getByText('Mi Biblioteca')).not.toBeVisible();
  });


  test('closes menu on link click', () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    const button = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(button);
    const link = screen.getByText('Mi Biblioteca');
    fireEvent.click(link);
    expect(screen.getByText('Mi Biblioteca')).not.toBeVisible();
  });


  test('renders all nav links', () => {
    render(
      <Router>
        <Header />
      </Router>
    );
    const button = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(button);
    expect(screen.getByText('Mi Biblioteca')).toBeInTheDocument();
    expect(screen.getByText('Añadir Libro')).toBeInTheDocument();
    expect(screen.getByText('Etiquetas')).toBeInTheDocument();
    expect(screen.getByText('Herramientas')).toBeInTheDocument();
    expect(screen.getByText('Charla sobre libros con la IA')).toBeInTheDocument();

  });

  test('handles HTTP error response', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    });
    render(
      <Router>
        <Header />
      </Router>
    );
    expect(await screen.findByText('No se pudo cargar el contador de libros. Inténtalo de nuevo más tarde.')).toBeInTheDocument();
  });

  test('handles null response from json', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => null });
    render(<Router><Header /></Router>);
    expect(await screen.findByText('0 libros en la biblioteca')).toBeInTheDocument();
  });

  test('handles undefined response from json', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => undefined });
    render(<Router><Header /></Router>);
    expect(await screen.findByText('0 libros en la biblioteca')).toBeInTheDocument();
  });


  test('handles non-number response from json', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => 'abc' });
    render(<Router><Header /></Router>);
    expect(await screen.findByText('0 libros en la biblioteca')).toBeInTheDocument();
  });

  test('handles fetch error gracefully', async () => {
    mockFetch.mockRejectedValue(new Error('Network error'));
    render(<Router><Header /></Router>);
    expect(await screen.findByText('No se pudo cargar el contador de libros. Inténtalo de nuevo más tarde.')).toBeInTheDocument();
  });

});