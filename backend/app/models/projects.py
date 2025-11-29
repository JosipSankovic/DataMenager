from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func, text
from app.core import Base # Correctly import Base from database module
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Project(Base):
    __tablename__ = "project"
    id = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String, nullable=True)
    absolute_path = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
