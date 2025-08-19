import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div data-testid="header">Header</div>);
jest.mock('./LibraryView', () => () => <div data-testid="library">Library</div>);
jest.mock('./UploadView', () => () => <div data-testid="upload">Upload</div>);
jest.mock('./CategoriesView', () => () => <div data-testid="categories">Categories</div>);
jest.mock('./ToolsView', () => () => <div data-testid="tools">Tools</div>);
jest.mock('./ReaderView', () => () => <div data-testid="reader">Reader</div>);
jest.mock('./RagView', () => () => <div data-testid="rag">Rag</div>);


test('renders App component', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByTestId('header')).toBeInTheDocument();
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('navigates to upload view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /Upload/i }));
  expect(screen.getByTestId('upload')).toBeInTheDocument();
});


test('navigates to categories view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /Etiquetas/i }));
  expect(screen.getByTestId('categories')).toBeInTheDocument();
});

test('navigates to tools view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /Herramientas/i }));
  expect(screen.getByTestId('tools')).toBeInTheDocument();
});

test('navigates to rag view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /Rag/i }));
  expect(screen.getByTestId('rag')).toBeInTheDocument();
});

test('navigates to reader view with bookId', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /Leer/i }));
  //This test needs improvement,  the implementation depends on the routing and how the link to /leer/:bookId is rendered.
});


test('renders LibraryView by default', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

```