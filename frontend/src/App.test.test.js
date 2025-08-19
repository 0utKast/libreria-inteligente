import React from 'react';
import { render, screen, fireEvent, Router, Route } from '@testing-library/react';
import App from './App';
import { MemoryRouter } from 'react-router-dom';
import { rest } from 'msw';
import { setupServer } from 'msw/node';


jest.mock('./Header', () => () => <div>Mocked Header</div>);
jest.mock('./LibraryView', () => () => <div>Mocked LibraryView</div>);
jest.mock('./UploadView', () => () => <div>Mocked UploadView</div>);
jest.mock('./CategoriesView', () => () => <div>Mocked CategoriesView</div>);
jest.mock('./ToolsView', () => () => <div>Mocked ToolsView</div>);
jest.mock('./ReaderView', () => ({ bookId }) => <div>Mocked ReaderView: {bookId}</div>);
jest.mock('./RagView', () => () => <div>Mocked RagView</div>);

const server = setupServer(
  //rest handlers if needed for API calls
)

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());


test('renders App component', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByText('Mocked Header')).toBeInTheDocument();
});

test('renders LibraryView on default route', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByText('Mocked LibraryView')).toBeInTheDocument();
});

test('renders UploadView on /upload route', () => {
  render(
    <MemoryRouter initialEntries={['/upload']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Mocked UploadView')).toBeInTheDocument();
});

test('renders CategoriesView on /etiquetas route', () => {
  render(
    <MemoryRouter initialEntries={['/etiquetas']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Mocked CategoriesView')).toBeInTheDocument();
});

test('renders ToolsView on /herramientas route', () => {
  render(
    <MemoryRouter initialEntries={['/herramientas']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Mocked ToolsView')).toBeInTheDocument();
});

test('renders RagView on /rag route', () => {
  render(
    <MemoryRouter initialEntries={['/rag']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Mocked RagView')).toBeInTheDocument();
});

test('renders ReaderView on /leer/:bookId route', () => {
  render(
    <MemoryRouter initialEntries={['/leer/123']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Mocked ReaderView: 123')).toBeInTheDocument();
});

test('handles empty bookId in ReaderView', () => {
    render(
      <MemoryRouter initialEntries={['/leer/']}>
        <App />
      </MemoryRouter>
    );
    // Expect appropriate handling of missing or invalid bookId.  This might involve error messages, redirects or fallback UI.  More specific expectation needed depending on App implementation.
    //Example: expect(screen.getByText('Error: Book ID is required')).toBeInTheDocument();
  });