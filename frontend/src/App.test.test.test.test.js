import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter, MemoryRouter } from 'react-router-dom';
import App from './App';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

jest.mock('./Header', () => () => <div>Header</div>);
jest.mock('./LibraryView', () => () => <div>LibraryView</div>);
jest.mock('./UploadView', () => () => <div>UploadView</div>);
jest.mock('./CategoriesView', () => () => <div>CategoriesView</div>);
jest.mock('./ToolsView', () => () => <div>ToolsView</div>);
jest.mock('./ReaderView', () => () => <div>ReaderView</div>);
jest.mock('./RagView', () => () => <div>RagView</div>);

const server = setupServer(
  // No REST handlers needed for this example as no API calls are made in the provided code.  Add them if your App component makes API calls.
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());


test('renders App component', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('Header')).toBeInTheDocument();
  expect(screen.getByText('LibraryView')).toBeInTheDocument();
});

test('navigates to /upload', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  fireEvent.click(screen.getByRole('link', { name: /upload/i }));
  expect(screen.getByText('UploadView')).toBeInTheDocument();
});


test('navigates to /etiquetas', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  fireEvent.click(screen.getByRole('link', { name: /etiquetas/i }));
  expect(screen.getByText('CategoriesView')).toBeInTheDocument();
});

test('navigates to /herramientas', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  fireEvent.click(screen.getByRole('link', { name: /herramientas/i }));
  expect(screen.getByText('ToolsView')).toBeInTheDocument();
});

test('navigates to /rag', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  fireEvent.click(screen.getByRole('link', { name: /rag/i }));
  expect(screen.getByText('RagView')).toBeInTheDocument();
});

test('navigates to /leer/:bookId', async () => {
  render(
    <MemoryRouter initialEntries={['/leer/123']}>
      <App />
    </MemoryRouter>
  );
  await waitFor(() => expect(screen.getByText('ReaderView')).toBeInTheDocument());
});


test('renders default route', () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('LibraryView')).toBeInTheDocument();
});

test('handles non existent route', () => {
  render(
    <MemoryRouter initialEntries={['/nonexistent']}>
      <App />
    </MemoryRouter>
  );
  expect(screen.getByText('LibraryView')).toBeInTheDocument(); 
});

```