# Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### 1. Backend Setup
```bash
cd s:\Yash_Project\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file with your credentials, then:
```bash
python init_db.py
python app.py
```

### 2. Frontend Setup
```bash
cd s:\Yash_Project\frontend
npm install
npm start
```

### 3. Test the System
1. Open http://localhost:3000
2. Paste a public Google Drive folder URL
3. Select storage provider (AWS S3 or Azure Blob)
4. Click "Import Images"
5. View imported images in the gallery

## 📝 Environment Variables Quick Reference

```env
# Required for AWS S3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=your-bucket

# Required for Azure Blob
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_STORAGE_CONTAINER_NAME=your-container

# Required for Database
DATABASE_URL=mssql+pyodbc://user:pass@server.database.windows.net:1433/db?driver=ODBC+Driver+17+for+SQL+Server

# Required for Google Drive
GOOGLE_DRIVE_API_KEY=your-api-key

# App Config
STORAGE_PROVIDER=aws_s3  # or azure_blob
SECRET_KEY=your-secret-key
```

## 🎯 Project Highlights

✅ **Multi-Cloud Support**: Seamlessly switch between AWS S3 and Azure Blob Storage  
✅ **Production-Ready**: Proper error handling, validation, and security  
✅ **Scalable Architecture**: Factory pattern for storage providers  
✅ **Clean Code**: Modular structure with separation of concerns  
✅ **Modern Stack**: Flask + React with best practices  
✅ **Database Persistence**: Azure SQL with SQLAlchemy ORM  
✅ **RESTful APIs**: Well-documented endpoints  

## 📂 What's Included

- ✅ Complete Flask backend with all routes
- ✅ Google Drive API integration
- ✅ AWS S3 storage service
- ✅ Azure Blob storage service
- ✅ Storage factory pattern
- ✅ Azure SQL database models
- ✅ Input validation utilities
- ✅ React frontend with modern UI
- ✅ API service layer
- ✅ Responsive CSS styling
- ✅ Comprehensive documentation
- ✅ Environment configuration
- ✅ Database initialization script

## 🔧 Next Steps

1. **Set up cloud resources**:
   - Create Azure SQL Database
   - Create S3 bucket or Azure Blob container
   - Set up Google Drive API credentials

2. **Configure environment**: Update `.env` with your credentials

3. **Run the application**: Start backend and frontend servers

4. **Test the system**: Import images and verify storage

## 💡 Tips

- Start with one storage provider (AWS S3 or Azure Blob)
- Use Google Drive's "Anyone with the link" sharing option
- Monitor cloud storage costs
- Implement rate limiting for production
- Add authentication for production use
- Consider adding image thumbnails for better performance
