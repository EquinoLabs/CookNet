from fastapi import HTTPException, APIRouter, File, UploadFile, Depends
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.user.enum import RoleEnum
from api.user.models import User
from api.user.auth import get_current_user
from api.cloudflare.r2_service import upload_media_file, get_presigned_url, delete_media_file
from api.stored_media.models import Media
from api.stored_media.schemas import MediaResponse, MediaOut
from database.database import get_db


router = APIRouter(prefix="/stored-media", tags=["stored-media"])

@router.get("/{media_id}", response_model=MediaResponse)
async def get_media_url(
    media_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Return presigned URL for media by ID"""
    try:
        # 1. lookup in DB
        result = await db.execute(select(Media).where(Media.id == media_id))
        media = result.scalars().first()

        if not media:
            raise HTTPException(status_code=404, detail="Media not found")

        # 2. generate presigned URL
        try:
            url = get_presigned_url(media.object_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not generate URL: {str(e)}")

        # 3. respond with safe info
        return MediaResponse(
            id=str(media.id),
            media_type=media.media_type,
            url=url,
            created_at=media.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving media: {str(e)}")


@router.post("/")
async def store_media(
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Store media in bucket"""
    try:
        # check role
        if current_user.role != RoleEnum.owner.value:
            raise HTTPException(status_code=403, detail="Only owners can upload media")

        if not any([image, video]):
            raise HTTPException(status_code=400, detail="Please upload either an image or video")

        if image and video:
            raise HTTPException(status_code=400, detail="Please upload either an image or video, not both")

        image_key: Optional[str] = None
        video_key: Optional[str] = None

        if image:
            object_key, media_type = await upload_media_file(image, current_user.id)
            if media_type == "image":
                image_key = object_key

        if video:
            object_key, media_type = await upload_media_file(video, current_user.id)
            if media_type == "video":
                video_key = object_key
        
        # save in DB
        media = Media(
            owner_id=current_user.id,
            object_key=object_key,   # full R2 path
            media_type=media_type,
        )
        db.add(media)

        # flush just pushes SQL to DB, but doesn’t commit
        await db.flush()
        await db.refresh(media)

        # now return response safely
        response = MediaOut.from_orm(media)

        # only commit at the very end
        await db.commit()
        return response
    except HTTPException:
        raise
    except Exception as e:
        # rollback DB
        await db.rollback()
        # delete uploaded files
        if image_key:
            await delete_media_file(image_key)
        if video_key:
            await delete_media_file(video_key)
        raise HTTPException(status_code=500, detail=f"Error uploading media: {str(e)}")
