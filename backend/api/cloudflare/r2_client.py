import boto3
import aiofiles
from botocore.config import Config
from fastapi import UploadFile, HTTPException
import os
import uuid
from uuid import UUID
from typing import Tuple
from datetime import datetime, timedelta
from threading import Lock
from collections import defaultdict

# in-memory cache for pre-signed url
url_cache = {}
locks = defaultdict(Lock)

class CloudflareR2Client:
    def __init__(self):
        # R2 uses S3-compatible API
        self.client = boto3.client(
            's3',
            endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
            region_name='auto',
            config=Config(signature_version='s3v4')
        )
        self.bucket_name = os.getenv('R2_BUCKET_NAME')
        self.public_url = f"https://{self.bucket_name}.{os.getenv('R2_ACCOUNT_ID')}.r2.dev"  # if public
    
    async def upload_file(self, file: UploadFile, user_id: UUID) -> Tuple[str, str]:
        """
        Upload file to R2 and return object key (to save in DB) and type
        """
        try:
            # Get file extension and type
            file_extension = file.filename.split('.')[-1]
            content_type = file.content_type or 'application/octet-stream'

            # Determine folder and media type
            if content_type.startswith('image/'):
                subfolder = "images"
                media_type = "image"
            elif content_type.startswith('video/'):
                subfolder = "video"
                media_type = "video"
            else:
                subfolder = "files"
                media_type = "file"

            # Create unique object key
            object_key = f"{user_id}/{subfolder}/{uuid.uuid4()}.{file_extension}"

            # Read file content
            file_content = await file.read()

            # Upload to R2
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    'user_id': str(user_id),
                    'original_filename': file.filename
                }
            )

            # Return object key, not URL
            return object_key, media_type

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    def get_presigned_url(self, object_key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for private object with caching + lock"""
        now = datetime.utcnow()

        # quick check without lock (fast path)
        if object_key in url_cache:
            url, expiry_time = url_cache[object_key]
            if expiry_time > now:
                return url

        # lock only when we need to regenerate
        with locks[object_key]:
            # check again inside lock (another thread may have already refreshed it)
            if object_key in url_cache:
                url, expiry_time = url_cache[object_key]
                if expiry_time > now:
                    return url

            # generate new URL
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_key},
                ExpiresIn=expires_in,
            )
            expiry_time = now + timedelta(seconds=expires_in - 60)  # renew a bit earlier
            url_cache[object_key] = (url, expiry_time)
            return url
    
    def is_bucket_public(self) -> bool:
        """Check if bucket is configured for public access"""
        # You'll need to implement this based on your bucket configuration
        return os.getenv('R2_BUCKET_PUBLIC', 'false').lower() == 'true'

    async def delete_file(self, file_key: str) -> bool:
        """Delete file from R2"""
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except:
            return False
