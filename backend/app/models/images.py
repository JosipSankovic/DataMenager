from app.core import Base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Images(Base):
    __tablename__="images"
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    project_id =  Column(UUID(as_uuid=True),ForeignKey("project.id"),nullable=False)
    rel_path = Column(String, index=True)

    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    channels = Column(Integer, default=3) # 3 for RGB, 1 for Grayscale

    mime_type = Column(String(50), default="image/jpeg")

    is_annotated = Column(Boolean,default=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

