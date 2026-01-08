import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Database Configuration
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server')
    
    # SQLAlchemy configuration
    # Try Azure SQL first, fall back to SQLite if credentials are missing
    if all([DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD]):
        # Azure SQL connection string with pyodbc
        # Format: mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
        connection_string = (
            f"DRIVER={{{DB_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        params = quote_plus(connection_string)
        SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    else:
        # Fallback to SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///images.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Cloud Storage Configuration
    STORAGE_PROVIDER = os.getenv('STORAGE_PROVIDER', 'aws')  # 'aws' or 'azure'
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    
    # Azure Configuration
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    
    # Google Drive API
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
