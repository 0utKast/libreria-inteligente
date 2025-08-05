import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { ReactReader } from 'react-reader';
import API_URL from './config';
import './ReaderView.css';

function ReaderView() {
  const { bookId } = useParams();
  const [location, setLocation] = useState(null);
  const [epubData, setEpubData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBookData = async () => {
      setIsLoading(true);
      setError('');
      try {
        const response = await fetch(`${API_URL}/books/download/${bookId}`);
        if (!response.ok) {
          throw new Error('No se pudo obtener el libro desde el servidor.');
        }
        const data = await response.arrayBuffer();
        setEpubData(data);
      } catch (err) {
        console.error("Error al obtener los datos del EPUB:", err);
        setError("No se pudo cargar el libro.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBookData();
  }, [bookId]);

  return (
    <div className="reader-container">
      <div className="reader-wrapper">
        {isLoading && <div className="loading-view">Cargando Libro...</div>}
        {error && <div className="loading-view">{error}</div>}
        {!isLoading && !error && epubData && (
          <ReactReader
            url={epubData}
            location={location}
            locationChanged={(epubcfi) => setLocation(epubcfi)}
            epubOptions={{
              flow: "paginated",
              spread: "auto"
            }}
          />
        )}
      </div>
    </div>
  );
}

export default ReaderView;