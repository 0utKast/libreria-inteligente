import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

jest.mock('./Header', () => () => <div>Header</div>);
jest.mock('./LibraryView', () => () => <div>LibraryView</div>);
jest.mock('./UploadView', () => () => <div>UploadView</div>);
jest.mock('./CategoriesView', () => () => <div>CategoriesView</div>);
jest.mock('./ToolsView', () => () => <div>ToolsView</div>);
jest.mock('./ReaderView', () => () => <div>ReaderView</div>);
jest.mock('./RagView', () => () => <div>RagView</div>);


test('renders App component', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByText('Header')).toBeInTheDocument();
  expect(screen.getByText('LibraryView')).toBeInTheDocument();
});

test('navigates to /upload', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /upload/i }));
  expect(screen.getByText('UploadView')).toBeInTheDocument();
});


test('navigates to /etiquetas', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /etiquetas/i }));
  expect(screen.getByText('CategoriesView')).toBeInTheDocument();
});

test('navigates to /herramientas', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /herramientas/i }));
  expect(screen.getByText('ToolsView')).toBeInTheDocument();
});

test('navigates to /rag', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  fireEvent.click(screen.getByRole('link', { name: /rag/i }));
  expect(screen.getByText('RagView')).toBeInTheDocument();
});

test('navigates to /leer/:bookId', () => {
    render(<BrowserRouter><App /></BrowserRouter>);
    //Simulate a link to /leer/123
    //This test requires a more robust solution to simulate dynamic routing.
    //The implementation would depend on the specific routing library used.
});


test('renders default route', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  expect(screen.getByText('LibraryView')).toBeInTheDocument();
});

```