import React, { useState, useCallback } from 'react';
import API_URL from './config';
import './ToolsView.css'; // Usaremos un CSS dedicado

function EpubToPdfConverter() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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

  const handleConvert = async () => {
    if (!selectedFile) {
      setMessage('Por favor, selecciona un archivo EPUB primero.');
      return;
    }
    if (!selectedFile.name.toLowerCase().endsWith('.epub')) {
      setMessage('El archivo seleccionado no es un EPUB.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    setIsLoading(true);
    setMessage('Convirtiendo archivo... Esto puede tardar un momento.');

    try {
      const response = await fetch(`${API_URL}/tools/convert-epub-to-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        // El backend ahora devuelve un JSON con la URL de descarga
        const result = await response.json();
        const downloadUrl = `${API_URL}${result.download_url}`;
        
        // Crear un enlace y hacer clic para iniciar la descarga
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = downloadUrl;
        a.target = '_blank'; // Abre en una nueva pestaña
        document.body.appendChild(a);
        a.click();
        
        // Limpiar el enlace del DOM
        document.body.removeChild(a);

        setMessage('¡Conversión completada! La descarga debería iniciarse.');
      } else {
        const result = await response.json();
        setMessage(`Error: ${result.detail || 'No se pudo procesar el archivo.'}`);
      }
    } catch (error) {
      setMessage('Error de conexión: No se pudo conectar con el backend.');
    } finally {
      setIsLoading(false);
      setSelectedFile(null);
    }
  };

  return (
    <div className="tool-card">
      <h3>Convertidor de EPUB a PDF</h3>
      <p>Sube un archivo EPUB para convertirlo a formato PDF.</p>
      <div className="upload-container" onDrop={handleDrop} onDragOver={handleDragOver}>
        <div className="drop-zone">
          {selectedFile ? <p>Archivo: {selectedFile.name}</p> : <p>Arrastra y suelta un archivo aquí, o usa el botón</p>}
          <input type="file" id="file-input-converter" onChange={handleFileChange} accept=".epub" />
          <label htmlFor="file-input-converter" className="file-label">Seleccionar archivo</label>
        </div>
        <button onClick={handleConvert} className="upload-button" disabled={isLoading}>
          {isLoading ? 'Convirtiendo...' : 'Convertir a PDF'}
        </button>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}


function ToolsView() {
  return (
    <div className="tools-container">
      <h2>Herramientas de la Biblioteca</h2>
      <div className="tools-grid">
        <EpubToPdfConverter />
        {/* Aquí se podrían añadir más herramientas en el futuro */}
      </div>
    </div>
  );
}

export default ToolsView;
