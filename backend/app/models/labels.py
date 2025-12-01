from app.core import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.sql import func
import uuid
#dont need label name because it is same as image
class Label(Base):
    __tablename__="labels"
    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id=Column(UUID(as_uuid=True),ForeignKey("images.id",ondelete="CASCADE"),nullable=False)
    version_id=Column(UUID(as_uuid=True),ForeignKey("versions.id", ondelete="CASCADE"),nullable=True)
    data = Column(JSONB,default={})
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    