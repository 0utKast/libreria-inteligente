import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div data-testid="header">Header</div>);
jest.mock('./LibraryView', () => () => <div data-testid="library">Library</div>);
jest.mock('./UploadView', () => () => <div data-testid="upload">Upload</div>);
jest.mock('./CategoriesView', () => () => <div data-testid="categories">Categories</div>);
jest.mock('./ToolsView', () => () => <div data-testid="tools">Tools</div>);
jest.mock('./ReaderView', () => ({ bookId }) => <div data-testid="reader">Reader {bookId}</div>);
jest.mock('./RagView', () => () => <div data-testid="rag">Rag</div>);


test('renders App component', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByTestId('header')).toBeInTheDocument();
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('navigates to upload view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const linkElement = screen.getByRole('link', { name: /upload/i });
  fireEvent.click(linkElement);
  expect(screen.getByTestId('upload')).toBeInTheDocument();
});

test('navigates to categories view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const linkElement = screen.getByRole('link', { name: /etiquetas/i });
  fireEvent.click(linkElement);
  expect(screen.getByTestId('categories')).toBeInTheDocument();
});

test('navigates to tools view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const linkElement = screen.getByRole('link', { name: /herramientas/i });
  fireEvent.click(linkElement);
  expect(screen.getByTestId('tools')).toBeInTheDocument();
});

test('navigates to rag view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const linkElement = screen.getByRole('link', { name: /rag/i });
  fireEvent.click(linkElement);
  expect(screen.getByTestId('rag')).toBeInTheDocument();
});

test('navigates to reader view with bookId', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const linkElement = screen.getByRole('link', { name: /leer\/123/i }); 
  fireEvent.click(linkElement);
  expect(screen.getByTestId('reader')).toHaveTextContent('Reader 123');
});

test('renders LibraryView by default', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByTestId('library')).toBeInTheDocument();
});

test('handles invalid bookId in reader view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const invalidLink = screen.queryByRole('link', { name: /leer\/abc/i });
  expect(invalidLink).toBeNull();
});

test('handles missing bookId in reader view', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const invalidLink = screen.queryByRole('link', { name: /leer\//i });
  expect(invalidLink).toBeNull();
});

```