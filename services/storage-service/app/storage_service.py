from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from azure.storage.blob import BlobServiceClient, ContentSettings
import base64
import io

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
STORAGE_PROVIDER = os.getenv('STORAGE_PROVIDER', 'azure')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

class StorageService:
    @staticmethod
    def upload_to_s3(file_buffer, filename, mime_type):
        """Upload file to AWS S3"""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            s3_client.upload_fileobj(
                file_buffer,
                AWS_BUCKET_NAME,
                unique_filename,
                ExtraArgs={'ContentType': mime_type, 'ACL': 'public-read'}
            )
            
            url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
            return {'success': True, 'url': url, 'provider': 'aws'}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upload_to_azure(file_buffer, filename, mime_type):
        """Upload file to Azure Blob Storage"""
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                AZURE_STORAGE_CONNECTION_STRING
            )
            
            unique_filename = f"{uuid.uuid4()}_{filename}"
            blob_client = blob_service_client.get_blob_client(
                container=AZURE_STORAGE_CONTAINER_NAME,
                blob=unique_filename
            )
            
            content_settings = ContentSettings(content_type=mime_type)
            blob_client.upload_blob(
                file_buffer,
                content_settings=content_settings,
                overwrite=True
            )
            
            url = blob_client.url
            return {'success': True, 'url': url, 'provider': 'azure'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_from_s3(file_path):
        """Delete file from AWS S3"""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            
            filename = file_path.split('/')[-1]
            s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=filename)
            return {'success': True}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_from_azure(file_path):
        """Delete file from Azure Blob Storage"""
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                AZURE_STORAGE_CONNECTION_STRING
            )
            
            blob_name = file_path.split('/')[-1]
            blob_client = blob_service_client.get_blob_client(
                container=AZURE_STORAGE_CONTAINER_NAME,
                blob=blob_name
            )
            blob_client.delete_blob()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'storage-service'}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload file to configured cloud storage"""
    try:
        data = request.get_json()
        file_data_base64 = data.get('file_data')  # Base64 encoded file
        filename = data.get('filename')
        mime_type = data.get('mime_type')
        provider = data.get('provider', STORAGE_PROVIDER)
        
        # Decode base64 to BytesIO
        file_bytes = base64.b64decode(file_data_base64)
        file_buffer = io.BytesIO(file_bytes)
        
        if provider == 'aws':
            result = StorageService.upload_to_s3(file_buffer, filename, mime_type)
        elif provider == 'azure':
            result = StorageService.upload_to_azure(file_buffer, filename, mime_type)
        else:
            return jsonify({'error': 'Invalid storage provider'}), 400
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_file():
    """Delete file from cloud storage"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        provider = data.get('provider', STORAGE_PROVIDER)
        
        if provider == 'aws':
            result = StorageService.delete_from_s3(file_path)
        elif provider == 'azure':
            result = StorageService.delete_from_azure(file_path)
        else:
            return jsonify({'error': 'Invalid storage provider'}), 400
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=False)
