from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
class ProjectCreate(BaseModel):
    name: str
    absolute_path: str
    description: str

class ProjectBase(BaseModel):
    id :UUID
    name : str
    description : str
    absolute_path : str
    created_at : datetime

