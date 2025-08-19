import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from './Header';
import '@testing-library/jest-dom';

jest.mock('./config', () => ({ default: 'http://test-api' }));

jest.mock('react-router-dom', () => ({
  NavLink: ({ to, children, onClick, className }) => (
    <a href={to} onClick={onClick} className={className}>
      {children}
    </a>
  ),
}));

describe('Header Component', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test('renders header component', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ count: 10 }),
    });
    render(<Header />);
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    expect(screen.getByText('📚 Librería Inteligente')).toBeInTheDocument();
    expect(await screen.findByText('10 libros en la biblioteca')).toBeInTheDocument();

  });

  test('renders error message when API call fails', async () => {
    global.fetch.mockRejectedValue(new Error('Failed to fetch'));
    render(<Header />);
    expect(await screen.findByText('No se pudo cargar el contador de libros. Inténtalo de nuevo más tarde.')).toBeInTheDocument();
  });

  test('toggles menu on hamburger click', () => {
    render(<Header />);
    const hamburgerButton = screen.getByRole('button', { name: /&#9776;/i });
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(true);
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('navigation').classList.contains('open')).toBe(false);
  });


  test('nav links call handleLinkClick', () => {
    const handleLinkClick = jest.fn();
    render(<Header handleLinkClick={handleLinkClick} />);
    const navLinks = screen.getAllByRole('link');
    navLinks.forEach(link => {
      fireEvent.click(link);
      expect(handleLinkClick).toHaveBeenCalled();
    });
  });

  test('updates book count when API call succeeds', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ count: 20 }),
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ count: 25 }),
    });
    render(<Header />);
    expect(await screen.findByText('20 libros en la biblioteca')).toBeInTheDocument();
    jest.advanceTimersByTime(600000);
    expect(await screen.findByText('25 libros en la biblioteca')).toBeInTheDocument();

  });
  
  test('handles empty book count', async () => {
    global.fetch.mockResolvedValue({
        ok: true,
        json: async () => ({ count: 0 }),
      });
      render(<Header />);
      expect(screen.queryByText(/libros en la biblioteca/i)).not.toBeInTheDocument();
  });


});
```