# Scalable Image Import System

A production-ready backend system built with Flask that imports images from public Google Drive folders and stores them in cloud object storage (AWS S3 or Azure Blob Storage) with metadata persistence in Azure SQL Database.

## 🚀 Features

### Backend
- **Multi-Cloud Storage Support**: AWS S3 and Azure Blob Storage
- **Google Drive Integration**: Import images from public Google Drive folders
- **Azure SQL Database**: Persistent metadata storage
- **RESTful APIs**: Clean, well-documented endpoints
- **Scalable Architecture**: Modular design with factory patterns
- **Error Handling**: Comprehensive error handling and validation
- **Environment-based Configuration**: Secure credential management

### Frontend
- **React Application**: Modern, responsive UI
- **Import Management**: Easy Google Drive folder URL input
- **Image Gallery**: Display imported images with metadata
- **Storage Provider Selection**: Choose between AWS S3 and Azure Blob
- **Real-time Feedback**: Loading states and error messages

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- Azure SQL Database
- AWS Account (for S3) or Azure Account (for Blob Storage)
- Google Cloud Platform account with Drive API enabled

## 🛠️ Installation

### Backend Setup

1. **Clone the repository**
```bash
cd s:\Yash_Project\backend
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**

Create a `.env` file in the `backend` directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration (Azure SQL)
DATABASE_URL=mssql+pyodbc://username:password@server.database.windows.net:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-s3-bucket-name

# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_STORAGE_CONTAINER_NAME=your-container-name

# Google Drive API Configuration
GOOGLE_DRIVE_API_KEY=your-google-drive-api-key

# Storage Provider (aws_s3 or azure_blob)
STORAGE_PROVIDER=aws_s3
```

5. **Initialize Database**
```bash
python init_db.py
```

6. **Run the backend**
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd s:\Yash_Project\frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure API endpoint**

Update `src/services/api.js` if your backend runs on a different port.

4. **Run the frontend**
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## 🔑 Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create credentials (API Key)
5. Add the API key to your `.env` file

### Making Google Drive Folder Public

1. Open Google Drive
2. Right-click on the folder
3. Click "Share"
4. Click "Change to anyone with the link"
5. Set permission to "Viewer"
6. Copy the folder URL

## 📚 API Documentation

### POST /api/import/google-drive

Import images from a public Google Drive folder.

**Request Body:**
```json
{
  "folder_url": "https://drive.google.com/drive/folders/FOLDER_ID",
  "storage_provider": "aws_s3"  // or "azure_blob"
}
```

**Response:**
```json
{
  "message": "Successfully imported 5 images",
  "images": [
    {
      "id": 1,
      "name": "image1.jpg",
      "google_drive_id": "abc123",
      "size": 1024000,
      "mime_type": "image/jpeg",
      "storage_path": "https://bucket.s3.amazonaws.com/image1.jpg",
      "storage_provider": "aws_s3",
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "failed": []
}
```

### GET /api/images

Retrieve all imported images with metadata.

**Query Parameters:**
- `storage_provider` (optional): Filter by storage provider (`aws_s3` or `azure_blob`)

**Response:**
```json
{
  "images": [
    {
      "id": 1,
      "name": "image1.jpg",
      "google_drive_id": "abc123",
      "size": 1024000,
      "mime_type": "image/jpeg",
      "storage_path": "https://bucket.s3.amazonaws.com/image1.jpg",
      "storage_provider": "aws_s3",
      "created_at": "2024-01-01T12:00:00"
    }
  ],
  "total": 1
}
```

### GET /api/images/:id

Get a specific image by ID.

**Response:**
```json
{
  "id": 1,
  "name": "image1.jpg",
  "google_drive_id": "abc123",
  "size": 1024000,
  "mime_type": "image/jpeg",
  "storage_path": "https://bucket.s3.amazonaws.com/image1.jpg",
  "storage_provider": "aws_s3",
  "created_at": "2024-01-01T12:00:00"
}
```

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Flask Backend  │
│   (REST API)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Azure  │ │ Cloud Storage│
│  SQL   │ │ (S3/Blob)    │
└────────┘ └──────────────┘
```

### Backend Structure

```
backend/
├── app.py                 # Application entry point
├── config.py             # Configuration management
├── models/
│   └── image.py         # SQLAlchemy models
├── routes/
│   ├── import_routes.py # Import endpoints
│   └── image_routes.py  # Image retrieval endpoints
├── services/
│   ├── google_drive_service.py  # Google Drive integration
│   ├── aws_s3_service.py        # AWS S3 storage
│   ├── azure_blob_service.py    # Azure Blob storage
│   └── storage_factory.py       # Storage provider factory
└── utils/
    ├── database.py      # Database utilities
    └── validators.py    # Input validation
```

## 🔒 Security Best Practices

- ✅ Environment variables for sensitive credentials
- ✅ Input validation and sanitization
- ✅ Error handling without exposing internals
- ✅ CORS configuration for production
- ✅ SQL injection prevention with SQLAlchemy ORM

## 🚀 Deployment

### Backend (Azure App Service)

1. Create Azure App Service (Python)
2. Configure environment variables in App Settings
3. Deploy using Git or Azure CLI
4. Ensure firewall rules allow App Service IP in Azure SQL

### Frontend (Vercel/Netlify)

1. Build the production bundle: `npm run build`
2. Deploy the `build` folder
3. Update API endpoint in production environment

## 🧪 Testing

### Test Import Endpoint
```bash
curl -X POST http://localhost:5000/api/import/google-drive \
  -H "Content-Type: application/json" \
  -d '{
    "folder_url": "https://drive.google.com/drive/folders/YOUR_FOLDER_ID",
    "storage_provider": "aws_s3"
  }'
```

### Test Get Images
```bash
curl http://localhost:5000/api/images
```

## 📈 Scalability Considerations

- **Async Processing**: Consider Celery for large batch imports
- **Caching**: Implement Redis for frequently accessed metadata
- **CDN**: Use CloudFront (AWS) or Azure CDN for image delivery
- **Database**: Connection pooling and indexing on frequently queried fields
- **Rate Limiting**: Implement rate limiting for API endpoints

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM
- **PyODBC**: Azure SQL connector
- **Boto3**: AWS SDK
- **Azure Storage Blob**: Azure SDK
- **Google API Client**: Google Drive integration

### Frontend
- **React**: UI framework
- **Axios**: HTTP client
- **CSS3**: Styling

## 📝 License

MIT License

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🐛 Troubleshooting

### Database Connection Issues
- Verify Azure SQL firewall rules
- Check ODBC Driver installation: `odbcinst -j`
- Test connection string

### Google Drive API Errors
- Ensure folder is public
- Verify API key is valid
- Check API quotas

### Storage Upload Failures
- Verify bucket/container exists
- Check IAM permissions (S3) or SAS tokens (Azure)
- Ensure credentials are correct

## 📞 Support

For issues and questions, please open an issue on GitHub.
