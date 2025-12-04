from pydantic import BaseModel,Field,ConfigDict,field_validator
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class LabelCreate(BaseModel):
    image_id : UUID
    version_id: Optional[UUID] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class LabelBase(LabelCreate):
    id :UUID
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)



class LabelUpdate(BaseModel):
    id :UUID
    version_id: Optional[UUID] = None
    data: Dict[str, Any] = Field(default_factory=dict)

class LabelAll(LabelBase):
    image_id : UUID
    version_id: Optional[UUID] = None
    data: Dict[str, Any] 
    model_config = ConfigDict(from_attributes=True)

    @field_validator('data',mode='before')
    @classmethod
    def ensure_dict(cls,v):
        if v is None:
            return {}
        return v
