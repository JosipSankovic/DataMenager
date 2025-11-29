from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    absolute_path: str
    description: str

class ProjectBase(BaseModel):
    id :int
    name : str
    description : str
    absolute_path : str
    created_at : datetime

