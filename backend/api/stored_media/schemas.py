from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MediaResponse(BaseModel):
    id: UUID
    media_type: str
    url: str
    created_at: datetime

    class Config:
        from_attributes = True

class MediaOut(BaseModel):
    id: UUID
    object_key: str
    media_type: str
    created_at: datetime

    class Config:
        from_attributes = True
