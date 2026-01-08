import React, { useState } from 'react';
import ImportForm from './components/ImportForm';
import ImageGallery from './components/ImageGallery';
import './App.css';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleImportComplete = () => {
    // Trigger refresh of image gallery
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1> Image Import System</h1>
        <p>Import images from Google Drive to Cloud Storage (AWS S3 / Azure Blob)</p>
      </header>
      
      <main className="App-main">
        <ImportForm onImportComplete={handleImportComplete} />
        <ImageGallery refreshTrigger={refreshTrigger} />
      </main>
      
      <footer className="App-footer">
        <p>Built with Flask, React, AWS S3, Azure Blob Storage, and Azure SQL</p>
      </footer>
    </div>
  );
}

export default App;
