import boto3
from botocore.exceptions import ClientError
from flask import current_app
import uuid

class S3StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'),
            region_name=current_app.config.get('AWS_REGION')
        )
        self.bucket_name = current_app.config.get('AWS_BUCKET_NAME')
    
    def upload_file(self, file_buffer, filename, mime_type):
        """Upload a file to S3"""
        try:
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Upload file
            self.s3_client.upload_fileobj(
                file_buffer,
                self.bucket_name,
                unique_filename,
                ExtraArgs={
                    'ContentType': mime_type,
                    'ACL': 'public-read'
                }
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.{current_app.config.get('AWS_REGION')}.amazonaws.com/{unique_filename}"
            
            return url
        except ClientError as e:
            raise Exception(f"Error uploading to S3: {str(e)}")
    
    def delete_file(self, file_path):
        """Delete a file from S3"""
        try:
            # Extract filename from URL
            filename = file_path.split('/')[-1]
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError as e:
            raise Exception(f"Error deleting from S3: {str(e)}")
