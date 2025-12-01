from pydantic import BaseModel,Field,ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class VersionCreate(BaseModel):
    project_id:UUID
    name:str

class VersionBase(BaseModel):
    id :UUID
    name: str
    created_at : datetime

