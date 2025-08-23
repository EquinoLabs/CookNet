from api.cloudflare.r2_client import CloudflareR2Client
from fastapi import UploadFile, HTTPException
from typing import Tuple
import os

# Initialize R2 client
r2_client = CloudflareR2Client()

async def upload_media_file(file: UploadFile, user_id: int) -> Tuple[str, str]:
    """
    Upload media file to R2 bucket
    Returns: (url, media_type)
    """
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 
                     'video/mp4', 'video/mpeg', 'video/quicktime']
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Check file size (adjust limit as needed for your 10GB quota)
    max_size = 100 * 1024 * 1024  # 100MB per file
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    
    return await r2_client.upload_file(file, user_id)

def get_presigned_url(object_key: str, expires_in: int = 3600) -> str:
    """
    Generate presigned URL for private object
    """
    return r2_client.get_presigned_url(object_key, expires_in)

async def delete_media_file(file_key: str) -> bool:
    """Delete media file from R2 using the object key stored in DB"""
    try:
        return await r2_client.delete_file(file_key)
    except:
        return False
