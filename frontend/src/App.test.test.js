import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div>Header Mock</div>);
jest.mock('./LibraryView', () => () => <div>LibraryView Mock</div>);
jest.mock('./UploadView', () => () => <div>UploadView Mock</div>);
jest.mock('./CategoriesView', () => () => <div>CategoriesView Mock</div>);
jest.mock('./ToolsView', () => () => <div>ToolsView Mock</div>);
jest.mock('./ReaderView', () => () => <div>ReaderView Mock</div>);
jest.mock('./RagView', () => () => <div>RagView Mock</div>);

test('renders App component', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByText('Header Mock')).toBeInTheDocument();
});

test('renders LibraryView on default route', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByText('LibraryView Mock')).toBeInTheDocument();
});

test('renders UploadView on /upload route', () => {
  render(<MemoryRouter initialEntries={['/upload']}><App /></MemoryRouter>);
  expect(screen.getByText('UploadView Mock')).toBeInTheDocument();
});

test('renders CategoriesView on /etiquetas route', () => {
  render(<MemoryRouter initialEntries={['/etiquetas']}><App /></MemoryRouter>);
  expect(screen.getByText('CategoriesView Mock')).toBeInTheDocument();
});

test('renders ToolsView on /herramientas route', () => {
  render(<MemoryRouter initialEntries={['/herramientas']}><App /></MemoryRouter>);
  expect(screen.getByText('ToolsView Mock')).toBeInTheDocument();
});

test('renders RagView on /rag route', () => {
  render(<MemoryRouter initialEntries={['/rag']}><App /></MemoryRouter>);
  expect(screen.getByText('RagView Mock')).toBeInTheDocument();
});

test('renders ReaderView with bookId', () => {
  render(<MemoryRouter initialEntries={['/leer/123']}><App /></MemoryRouter>);
  expect(screen.getByText('ReaderView Mock')).toBeInTheDocument();
});

test('renders 404 for invalid route', () => {
  render(<MemoryRouter initialEntries={['/invalid-route']}><App /></MemoryRouter>);
  expect(screen.queryByText('LibraryView Mock')).not.toBeInTheDocument();
});

test('App handles empty routes gracefully', () => {
  render(<MemoryRouter initialEntries={['']}><App /></MemoryRouter>);
  expect(screen.getByText('LibraryView Mock')).toBeInTheDocument();
});

test('App handles null routes gracefully', () => {
  render(<MemoryRouter initialEntries={[null]}><App /></MemoryRouter>);
  expect(screen.getByText('LibraryView Mock')).toBeInTheDocument();
});

test('App handles undefined routes gracefully', () => {
  render(<MemoryRouter initialEntries={[undefined]}><App /></MemoryRouter>);
  expect(screen.getByText('LibraryView Mock')).toBeInTheDocument();
});