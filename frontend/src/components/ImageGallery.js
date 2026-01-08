import React, { useState, useEffect } from 'react';
import { getImages, deleteImage, getStats } from '../services/api';
import './ImageGallery.css';

const ImageGallery = ({ refreshTrigger }) => {
  const [images, setImages] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchImages();
    fetchStats();
  }, [page, refreshTrigger]);

  const fetchImages = async () => {
    try {
      setLoading(true);
      const data = await getImages(page, 20);
      setImages(data.images);
      setTotalPages(data.total_pages);
      setError(null);
    } catch (err) {
      setError('Failed to load images');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const data = await getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handleDelete = async (imageId) => {
    if (window.confirm('Are you sure you want to delete this image?')) {
      try {
        await deleteImage(imageId);
        fetchImages();
        fetchStats();
      } catch (err) {
        alert('Failed to delete image');
      }
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="image-gallery-container">
      <h2>Imported Images</h2>

      {stats && (
        <div className="stats-panel">
          <div className="stat-card">
            <h3>{stats.total_images}</h3>
            <p>Total Images</p>
          </div>
          <div className="stat-card">
            <h3>{stats.total_size_mb} MB</h3>
            <p>Total Storage</p>
          </div>
          <div className="stat-card">
            <h3>{stats.aws_images}</h3>
            <p>AWS S3</p>
          </div>
          <div className="stat-card">
            <h3>{stats.azure_images}</h3>
            <p>Azure Blob</p>
          </div>
        </div>
      )}

      {loading && <div className="loading">Loading images...</div>}

      {error && <div className="error">{error}</div>}

      {!loading && images.length === 0 && (
        <div className="no-images">
          <p>No images imported yet. Use the form above to import images from Google Drive.</p>
        </div>
      )}

      <div className="image-grid">
        {images.map((image) => (
          <div key={image.id} className="image-card">
            <div className="image-preview">
              <img src={image.storage_path} alt={image.name} />
            </div>
            <div className="image-info">
              <h4>{image.name}</h4>
              <p className="image-meta">
                <span className="badge">{image.storage_provider.toUpperCase()}</span>
                <span>{formatBytes(image.size)}</span>
              </p>
              <p className="image-meta">
                <span>{image.mime_type}</span>
              </p>
              <div className="image-actions">
                <a 
                  href={image.storage_path} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn-secondary"
                >
                  View
                </a>
                <button 
                  onClick={() => handleDelete(image.id)}
                  className="btn-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button 
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="btn-secondary"
          >
            Previous
          </button>
          <span>Page {page} of {totalPages}</span>
          <button 
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="btn-secondary"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default ImageGallery;
