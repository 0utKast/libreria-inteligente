import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div data-testid="header">Header</div>);
jest.mock('./LibraryView', () => () => <div data-testid="library">Library</div>);
jest.mock('./UploadView', () => () => <div data-testid="upload">Upload</div>);
jest.mock('./CategoriesView', () => () => <div data-testid="categories">Categories</div>);
jest.mock('./ToolsView', () => () => <div data-testid="tools">Tools</div>);
jest.mock('./ReaderView', () => ({ bookId }) => <div data-testid="reader">{bookId}</div>);
jest.mock('./RagView', () => () => <div data-testid="rag">Rag</div>);


test('renders App component', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByTestId('header')).toBeInTheDocument();
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('navigates to upload view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  fireEvent.click(screen.getByRole('link', { name: /upload/i }));
  expect(screen.getByTestId('upload')).toBeInTheDocument();
});

test('navigates to categories view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  fireEvent.click(screen.getByRole('link', { name: /etiquetas/i }));
  expect(screen.getByTestId('categories')).toBeInTheDocument();
});

test('navigates to tools view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  fireEvent.click(screen.getByRole('link', { name: /herramientas/i }));
  expect(screen.getByTestId('tools')).toBeInTheDocument();
});

test('navigates to rag view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  fireEvent.click(screen.getByRole('link', { name: /rag/i }));
  expect(screen.getByTestId('rag')).toBeInTheDocument();
});

test('navigates to reader view with bookId', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  fireEvent.click(screen.getByRole('link', { name: /leer\/123/i }));
  expect(screen.getByTestId('reader')).toHaveTextContent('123');
});


test('renders default view when path is invalid', () => {
  render(<MemoryRouter initialEntries={['/invalid-path']}><App /></MemoryRouter>);
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('handles missing bookId in reader view', () => {
    render(<MemoryRouter initialEntries={['/leer/']}><App /></MemoryRouter>);
    expect(screen.getByTestId('library')).toBeInTheDocument();
  });

test('handles non-numeric bookId in reader view', () => {
    render(<MemoryRouter initialEntries={['/leer/abc']}><App /></MemoryRouter>);
    expect(screen.getByTestId('library')).toBeInTheDocument();
  });

```