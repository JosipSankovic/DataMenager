from fastapi import APIRouter, Depends, HTTPException
from app.schemas import LabelBase,LabelCreate
from app.core import get_db
from sqlalchemy.orm import Session
from app.services import LabelsService

router = APIRouter(prefix="/labels",tags=["labels"])

label_serive = LabelsService()

@router.get("/",response_model=list[LabelBase])
def get_labels(version_id:str,project_id:str,use_non_versioned:bool=True,offset: int = 0, limit: int = 10000,db:Session = Depends(get_db))->list[LabelBase]:
    labels=label_serive.get_version_labels(version_id,project_id,db,use_non_versioned,offset,limit)
    return labels


@router.post("/",response_model=LabelBase)
def add_label(label:LabelCreate,db:Session = Depends(get_db))->LabelBase:
    label=label_serive.add_label(label,db)
    return label

