import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Header from './Header';
import { BrowserRouter as Router } from 'react-router-dom';

jest.mock('./config', () => ({ API_URL: '/api' }));

const mockFetch = jest.spyOn(global, 'fetch');

afterEach(() => {
  jest.clearAllMocks();
});

test('renders Header component', () => {
  mockFetch.mockResolvedValue({ ok: true, json: async () => 10 });
  render(<Router><Header /></Router>);
  expect(screen.getByText(/📚 Librería Inteligente/i)).toBeInTheDocument();
});

test('displays book count and handles errors', async () => {
  mockFetch.mockResolvedValueOnce({ ok: true, json: async () => 10 });
  render(<Router><Header /></Router>);
  expect(await screen.findByText(/10 libros en la biblioteca/i)).toBeInTheDocument();

  mockFetch.mockRejectedValueOnce(new Error('Network error'));
  fireEvent.click(screen.getByRole('button')); 
  expect(await screen.findByText(/No se pudo cargar el contador de libros/i)).toBeInTheDocument();
});

test('toggles menu on hamburger click', () => {
  mockFetch.mockResolvedValue({ ok: true, json: async () => 0 });
  render(<Router><Header /></Router>);
  const menuButton = screen.getByRole('button', { name: /hamburguer/i });
  fireEvent.click(menuButton);
  expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
  fireEvent.click(menuButton);
  expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);
});

test('closes menu on link click', () => {
  mockFetch.mockResolvedValue({ ok: true, json: async () => 0 });
  render(<Router><Header /></Router>);
  const menuButton = screen.getByRole('button', { name: /hamburguer/i });
  fireEvent.click(menuButton);
  expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
  fireEvent.click(screen.getByRole('link', { name: /Mi Biblioteca/i }));
  expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);
});


test('nav links render correctly', () => {
  mockFetch.mockResolvedValue({ ok: true, json: async () => 0 });
  render(<Router><Header /></Router>);
  expect(screen.getByRole('link', { name: /Mi Biblioteca/i })).toBeInTheDocument();
  expect(screen.getByRole('link', { name: /Añadir Libro/i })).toBeInTheDocument();
  expect(screen.getByRole('link', { name: /Etiquetas/i })).toBeInTheDocument();
  expect(screen.getByRole('link', { name: /Herramientas/i })).toBeInTheDocument();
  expect(screen.getByRole('link', { name: /Charla sobre libros con la IA/i })).toBeInTheDocument();
});

test('handles fetch errors gracefully', async () => {
  mockFetch.mockRejectedValue(new Error('Failed to fetch'));
  render(<Router><Header /></Router>);
  await waitFor(() => expect(screen.getByText(/No se pudo cargar el contador de libros/i)).toBeInTheDocument());
});

test('displays zero books when fetch returns zero', async () => {
  mockFetch.mockResolvedValue({ ok: true, json: async () => 0 });
  render(<Router><Header /></Router>);
  await waitFor(() => expect(screen.getByText(/0 libros en la biblioteca/i)).toBeInTheDocument());
});

test('renders correctly with no API_URL', () => {
  jest.mock('./config', () => ({})); //Simulate missing API_URL
  render(<Router><Header /></Router>);
  expect(screen.getByText(/📚 Librería Inteligente/i)).toBeInTheDocument();
  expect(screen.queryByText(/No se pudo cargar el contador de libros/i)).not.toBeInTheDocument();

});

test('shows loading indicator while fetching', async () => {
  const mockJson = jest.fn().mockResolvedValue(10);
  const mockFetchPromise = Promise.resolve({ok:true, json: mockJson});

  mockFetch.mockImplementationOnce(() => mockFetchPromise);
  render(<Router><Header /></Router>);
  expect(screen.getByText(/Cargando.../i)).toBeInTheDocument(); //Check loading indicator
  await waitFor(() => expect(mockJson).toHaveBeenCalled()); // wait for fetch to resolve
  expect(screen.queryByText(/Cargando.../i)).not.toBeInTheDocument()); //Check loading indicator gone


});

```