from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List, Dict, Union, Any

AugmentationValue = Union[List[float], float, int]

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

class ImageMetadata(BaseModel):
    image_id: UUID
    version_id: UUID
    rel_path: str
    augmentations: Dict[str, AugmentationValue] = {}
