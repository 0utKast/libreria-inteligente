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
  fireEvent.click(screen.getByRole('link', { name: /upload/i }));
  expect(screen.getByTestId('upload')).toBeInTheDocument();
});

test('navigates to categories view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /etiquetas/i }));
  expect(screen.getByTestId('categories')).toBeInTheDocument();
});

test('navigates to tools view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /herramientas/i }));
  expect(screen.getByTestId('tools')).toBeInTheDocument();
});

test('navigates to rag view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /rag/i }));
  expect(screen.getByTestId('rag')).toBeInTheDocument();
});

test('navigates to reader view with bookId', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /leer\/123/i }));
  expect(screen.getByTestId('reader')).toBeInTheDocument();
});


test('renders default view when path is invalid', () => {
    render(<BrowserRouter><App /></BrowserRouter>, {route: '/invalid-path'});
    expect(screen.getByTestId('library')).toBeInTheDocument();

});

```