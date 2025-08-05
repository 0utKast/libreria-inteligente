import React, { useState, useCallback } from 'react';
import API_URL from './config';
import './RagView.css';

function RagView() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [bookId, setBookId] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentQuery, setCurrentQuery] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMessage('');
  };

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      setSelectedFile(event.dataTransfer.files[0]);
      setMessage('');
      event.dataTransfer.clearData();
    }
  }, []);

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Por favor, selecciona un archivo PDF o EPUB primero.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    setIsLoading(true);
    setMessage('Procesando libro para RAG... Esto puede tardar un momento.');

    try {
      const response = await fetch(`${API_URL}/rag/upload-book/`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setBookId(result.book_id);
        setMessage('Libro procesado exitosamente. ¡Ahora puedes hacer preguntas!');
        setChatHistory([]); // Clear chat history for new book
      } else {
        const result = await response.json();
        setMessage(`Error: ${result.detail || 'No se pudo procesar el libro para RAG.'}`);
      }
    } catch (error) {
      setMessage('Error de conexión: No se pudo conectar con el backend.');
    } finally {
      setIsLoading(false);
      setSelectedFile(null);
    }
  };

  const handleQuerySubmit = async (event) => {
    event.preventDefault();
    if (!bookId || !currentQuery.trim()) {
      return;
    }

    const newChatHistory = [...chatHistory, { sender: 'user', text: currentQuery }];
    setChatHistory(newChatHistory);
    setCurrentQuery('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/rag/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: currentQuery, book_id: bookId }),
      });

      if (response.ok) {
        const result = await response.json();
        setChatHistory([...newChatHistory, { sender: 'gemini', text: result.response }]);
      } else {
        const result = await response.json();
        setChatHistory([...newChatHistory, { sender: 'gemini', text: `Error: ${result.detail || 'No se pudo obtener respuesta.'}` }]);
      }
    } catch (error) {
      setChatHistory([...newChatHistory, { sender: 'gemini', text: 'Error de conexión al consultar.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rag-container">
      <h2>Conversación Inteligente con Libros</h2>
      <p>Sube un libro (PDF o EPUB) para conversar con la IA sobre su contenido.</p>

      <div className="upload-section" onDrop={handleDrop} onDragOver={handleDragOver}>
        <div className="drop-zone">
          {selectedFile ? <p>Archivo: {selectedFile.name}</p> : <p>Arrastra y suelta un archivo aquí, o usa el botón</p>}
          <input type="file" id="rag-file-input" onChange={handleFileChange} accept=".pdf,.epub" />
          <label htmlFor="rag-file-input" className="file-label">Seleccionar archivo</label>
        </div>
        <button onClick={handleUpload} className="upload-button" disabled={isLoading || !selectedFile}>
          {isLoading ? 'Procesando...' : 'Procesar libro para conversar'}
        </button>
        {message && <p className="message">{message}</p>}
      </div>

      {bookId && (
        <div className="chat-section">
          <h3>Conversación sobre el libro</h3>
          <div className="chat-history">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                <strong>{msg.sender === 'user' ? 'Tú' : 'Gemini'}:</strong> {msg.text}
              </div>
            ))}
          </div>
          <form onSubmit={handleQuerySubmit} className="chat-input-form">
            <input
              type="text"
              value={currentQuery}
              onChange={(e) => setCurrentQuery(e.target.value)}
              placeholder="Haz una pregunta sobre el libro..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !currentQuery.trim()}>
              Enviar
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

export default RagView;
