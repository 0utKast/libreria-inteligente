import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter, MemoryRouter, Routes, Route } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div data-testid="header">Header</div>);
jest.mock('./LibraryView', () => () => <div data-testid="library">Library</div>);
jest.mock('./UploadView', () => () => <div data-testid="upload">Upload</div>);
jest.mock('./CategoriesView', () => () => <div data-testid="categories">Categories</div>);
jest.mock('./ToolsView', () => () => <div data-testid="tools">Tools</div>);
jest.mock('./ReaderView', () => ({ bookId }) => <div data-testid="reader">Reader {bookId || ''}</div>);
jest.mock('./RagView', () => () => <div data-testid="rag">Rag</div>);


test('renders App component', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByTestId('header')).toBeInTheDocument();
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('navigates to upload view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const uploadLink = screen.getByRole('link', { name: /upload/i });
  fireEvent.click(uploadLink);
  expect(screen.getByTestId('upload')).toBeInTheDocument();
});

test('navigates to categories view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const categoriesLink = screen.getByRole('link', { name: /etiquetas/i });
  fireEvent.click(categoriesLink);
  expect(screen.getByTestId('categories')).toBeInTheDocument();
});

test('navigates to tools view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const toolsLink = screen.getByRole('link', { name: /herramientas/i });
  fireEvent.click(toolsLink);
  expect(screen.getByTestId('tools')).toBeInTheDocument();
});

test('navigates to rag view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const ragLink = screen.getByRole('link', { name: /rag/i });
  fireEvent.click(ragLink);
  expect(screen.getByTestId('rag')).toBeInTheDocument();
});

test('navigates to reader view with bookId', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const readerLink = screen.getByRole('link', { name: /leer\/123/i });
  fireEvent.click(readerLink);
  expect(screen.getByTestId('reader')).toHaveTextContent('Reader 123');
});

test('navigates to reader view with different bookId', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const readerLink = screen.getByRole('link', { name: /leer\/456/i });
  fireEvent.click(readerLink);
  expect(screen.getByTestId('reader')).toHaveTextContent('Reader 456');
});


test('renders default library view', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('handles missing bookId in reader link', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const readerLink = screen.getByRole('link', { name: /leer/i });
  fireEvent.click(readerLink);
  expect(screen.getByTestId('reader')).toHaveTextContent('Reader ');
});

test('handles invalid bookId in reader link', () => {
  render(<MemoryRouter><App /></MemoryRouter>);
  const readerLink = screen.getByRole('link', { name: /leer\/abc/i });
  fireEvent.click(readerLink);
  expect(screen.getByTestId('reader')).toHaveTextContent('Reader ');
});

test('renders error message for invalid routes', () => {
  render(
    <MemoryRouter initialEntries={['/invalid']}>
      <Routes>
        <Route path="*" element={<App />} />
      </Routes>
    </MemoryRouter>
  );
  expect(screen.getByText(/Error: Invalid route/i)).toBeInTheDocument();
});