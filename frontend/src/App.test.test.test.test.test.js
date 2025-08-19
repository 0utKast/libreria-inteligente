import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
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

const server = setupServer();

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
  expect(screen.getByText('Mocked ReaderView: undefined')).toBeInTheDocument();
});

test('handles invalid bookId in ReaderView', () => {
  render(
    <MemoryRouter initialEntries={['/leer/abc']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Mocked ReaderView: abc')).toBeInTheDocument();
});

test('handles null bookId in ReaderView', () => {
    render(
      <MemoryRouter initialEntries={['/leer/null']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Mocked ReaderView: null')).toBeInTheDocument();
  });

  test('handles undefined bookId in ReaderView', () => {
    render(
      <MemoryRouter initialEntries={['/leer/undefined']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Mocked ReaderView: undefined')).toBeInTheDocument();
  });


test('handles no bookId in ReaderView', () => {
    render(
      <MemoryRouter initialEntries={['/leer']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Mocked ReaderView: undefined')).toBeInTheDocument();
  });


//Simulacion de fetch, requiere que App use fetch
// test('fetches data and updates UI', async () => {
//   const mockData = [{ id: 1, title: 'Test Book' }];
//   const mockFetch = jest.spyOn(window, 'fetch').mockResolvedValue({
//     json: () => Promise.resolve(mockData),
//   });

//   render(<MemoryRouter><App /></MemoryRouter>);

//   await screen.findByText('Test Book'); // Or some other indicator of data being displayed
//   expect(mockFetch).toHaveBeenCalled();
//   mockFetch.mockRestore();
// });

//Add more tests as needed based on the actual App component implementation.  These are examples and need to be adapted.