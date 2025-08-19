import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div>Header Mock</div>);
jest.mock('./LibraryView', () => () => <div>LibraryView Mock</div>);
jest.mock('./UploadView', () => () => <div>UploadView Mock</div>);
jest.mock('./CategoriesView', () => () => <div>CategoriesView Mock</div>);
jest.mock('./ToolsView', () => () => <div>ToolsView Mock</div>);
jest.mock('./ReaderView', () => () => <div>ReaderView Mock</div>);
jest.mock('./RagView', () => () => <div>RagView Mock</div>);


test('renders App component', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByText('Header Mock')).toBeInTheDocument();
});

test('renders LibraryView on default route', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByText('LibraryView Mock')).toBeInTheDocument();
});


test('renders UploadView on /upload route', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>, { route: '/upload' }
  );
  expect(screen.getByText('UploadView Mock')).toBeInTheDocument();
});

test('renders CategoriesView on /etiquetas route', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>, { route: '/etiquetas' }
  );
  expect(screen.getByText('CategoriesView Mock')).toBeInTheDocument();
});

test('renders ToolsView on /herramientas route', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>, { route: '/herramientas' }
  );
  expect(screen.getByText('ToolsView Mock')).toBeInTheDocument();
});

test('renders RagView on /rag route', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>, { route: '/rag' }
  );
  expect(screen.getByText('RagView Mock')).toBeInTheDocument();
});

test('renders ReaderView with bookId', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>, { route: '/leer/123' }
  );
  expect(screen.getByText('ReaderView Mock')).toBeInTheDocument();
});

test('renders 404 for invalid route', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>, { route: '/invalid-route' }
  );
  expect(screen.queryByText('LibraryView Mock')).not.toBeInTheDocument(); // Example, adapt to your 404 handling.  
});