from app.core import Base
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
import uuid
from app.schemas import DatasetData
# Table for dataset versioning. 
# In data column will be images with their
# corresponding versions and augmentation step

class Dataset(Base):
    __tablename__="dataset"
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    project_id =  Column(UUID(as_uuid=True),ForeignKey("project.id"),nullable=False)
    version_id =  Column(UUID(as_uuid=True),ForeignKey("versions.id"),nullable=False)
    name = Column(String)
    description = Column(String,nullable=True)
    data = Column(JSONB,default={"train": [],"valid": [],"test": []})
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())
    
    @validates("data")
    def validate_data(self, key, value):
        if isinstance(value,DatasetData):
            return value.model_dump(mode="json")
        if isinstance(value,dict):
            return DatasetData(**value).model_dump(mode='json')
        raise ValueError(f"Expected dict or DatasetData, got {type(value)}")