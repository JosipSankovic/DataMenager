from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ImageBase(BaseModel):
    id:UUID
    project_id:UUID
    rel_path:str
    width:int
    height:int
    channels:int
    mime_type:str
    is_annotated:bool
    created_at:datetime

class ImageCreate(BaseModel):
    project_id:UUID
    rel_path:str
    width:int
    height:int
    channels:int
    mime_type:str
    is_annotated:bool
    created_at:datetime
    class Config:
        from_attributes = True

class ImageIds(BaseModel):
    id:UUID
    rel_path:str

class ImageDelete(BaseModel):
    id:UUID