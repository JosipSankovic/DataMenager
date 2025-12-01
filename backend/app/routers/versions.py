from fastapi import APIRouter, Depends, HTTPException
from app.schemas import VersionBase,VersionCreate
from app.core import get_db
from sqlalchemy.orm import Session
from app.services import VersionService

router = APIRouter(prefix="/versions",tags=["versions"])

version_service = VersionService()

@router.get("/",response_model=list[VersionBase])
def get_versions(project_id=str,offset: int = 0, limit: int = 100,db:Session = Depends(get_db))->list[VersionBase]:
    version=version_service.get_versions(project_id,db)
    return version


@router.post("/",response_model=VersionBase)
def add_version(version:VersionCreate,db:Session = Depends(get_db))->VersionBase:
    db_version = version_service.add_version(version,db)
    return db_version
