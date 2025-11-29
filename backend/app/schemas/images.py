from pydantic import BaseModel
from datetime import datetime

class ImageBase(BaseModel):
    id:str
    project_id:str
    rel_path:str
    width:int
    height:int
    channels:int
    mime_type:str
    is_annotated:bool
    created_at:datetime

class ImageCreate(BaseModel):
    project_id:str
    rel_path:str
    width:int
    height:int
    channels:int
    mime_type:str
    is_annotated:bool