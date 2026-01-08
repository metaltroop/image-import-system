from azure.storage.blob import BlobServiceClient, ContentSettings
from flask import current_app
import uuid

class AzureBlobStorageService:
    def __init__(self):
        self.connection_string = current_app.config.get('AZURE_STORAGE_CONNECTION_STRING')
        self.container_name = current_app.config.get('AZURE_STORAGE_CONTAINER_NAME')
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        
    def upload_file(self, file_buffer, filename, mime_type):
        """Upload a file to Azure Blob Storage"""
        try:
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Get blob client
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=unique_filename
            )
            
            # Upload file
            content_settings = ContentSettings(content_type=mime_type)
            blob_client.upload_blob(
                file_buffer,
                content_settings=content_settings,
                overwrite=True
            )
            
            # Generate URL
            url = blob_client.url
            
            return url
        except Exception as e:
            raise Exception(f"Error uploading to Azure Blob Storage: {str(e)}")
    
    def delete_file(self, file_path):
        """Delete a file from Azure Blob Storage"""
        try:
            # Extract blob name from URL
            blob_name = file_path.split('/')[-1]
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.delete_blob()
            return True
        except Exception as e:
            raise Exception(f"Error deleting from Azure Blob Storage: {str(e)}")
