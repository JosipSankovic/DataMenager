from fastapi import APIRouter, Depends, HTTPException
from app.schemas import LabelBase,LabelCreate
from app.core import get_db
from sqlalchemy.orm import Session
from app.services import LabelsService

router = APIRouter(prefix="/labels",tags=["labels"])

label_service = LabelsService()

@router.get("/",response_model=list[LabelBase])
def get_labels(version_id:str,project_id:str,use_non_versioned:bool=True,offset: int = 0, limit: int = 10000,db:Session = Depends(get_db))->list[LabelBase]:
    labels=label_service.get_version_labels(version_id,project_id,db,use_non_versioned,offset,limit)
    return labels

@router.get("/get-image-label",response_model=LabelBase)
def get_image_label(image_id:str,version_id:str = None,db:Session=Depends(get_db))->LabelBase:
    db_label = label_service.get_image_label(image_id,db,version_id)
    if db_label is None:
        raise HTTPException(status_code=404,detail="Cant find label for image")
    return db_label

@router.post("/",response_model=LabelBase)
def add_label(label:LabelCreate,db:Session = Depends(get_db))->LabelBase:
    label=label_service.add_label(label,db)
    return label

