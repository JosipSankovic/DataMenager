from pydantic import BaseModel,Field,ConfigDict
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

