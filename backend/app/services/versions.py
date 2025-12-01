from app.models import Version
from sqlalchemy.orm import Session
from sqlalchemy import insert,desc
from app.schemas import VersionBase, VersionCreate
import os
from fastapi import HTTPException
import cv2
import numpy as np
import shutil
import uuid
from datetime import datetime,timezone


class VersionService:


    def get_versions(self,project_id:str,db:Session)->list[VersionBase]:
        versions = db.query(Version).filter(Version.project_id==project_id).order_by(desc(Version.created_at)).all()
        return versions
    
    def get_version(self,version_id:str,db:Session)->VersionBase:
        version = db.query(Version).filter(Version.id == version_id).first()
        if not version:
            raise HTTPException(status_code=404,detail="Version not found")
        return version

    def add_version(self,version:VersionCreate,db:Session)->VersionBase:
        from app.services import LabelsService
        label_service = LabelsService()
        db_version=Version(
            project_id = version.project_id,
            name = version.name
        )
        print(db_version)
        db.add(db_version)
        db.commit()
        label_service.apply_version(version_id=db_version.id,project_id=version.project_id,db=db)
        return db_version