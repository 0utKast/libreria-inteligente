import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './Header';
import LibraryView from './LibraryView';
import UploadView from './UploadView';
import CategoriesView from './CategoriesView';
import ToolsView from './ToolsView';
import ReaderView from './ReaderView';
import RagView from './RagView';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Header />
        <main className="App-content">
          <Routes>
            <Route path="/" element={<LibraryView />} />
            <Route path="/upload" element={<UploadView />} />
            <Route path="/etiquetas" element={<CategoriesView />} />
            <Route path="/herramientas" element={<ToolsView />} />
            <Route path="/rag" element={<RagView />} />
            <Route path="/leer/:bookId" element={<ReaderView />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;