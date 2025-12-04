from fastapi import APIRouter, Depends, HTTPException
from app.core import get_db
from sqlalchemy.orm import Session
from app.schemas import DatasetBase,DatasetData,DatasetAll,DatasetCreate,LabelDataset,ImageMetadata
from app.services import DatasetService


router = APIRouter(prefix="/dataset",tags=["dataset"])
dataset_service = DatasetService()
@router.get("/all",response_model=list[DatasetBase])
def get_all(project_id:str,db:Session=Depends(get_db))->list[DatasetBase]:
    datasets = dataset_service.get_all_datasets(project_id,db)
    return datasets
@router.post("/allver",response_model=DatasetAll)
def get_all(dataset:DatasetCreate,db:Session=Depends(get_db))->DatasetAll:
    labels=dataset_service.create_automatic_dataset(db,dataset)
    return labels

@router.get("/",response_model=list[DatasetBase])
def get(dataset_id:str,project_id:str,db:Session=Depends(get_db))->DatasetBase:
    pass


@router.post("/",response_model=DatasetBase)
def create_dataset(dataset:DatasetCreate,db:Session=Depends(get_db))->DatasetBase:
    db_dataset = dataset_service.create_dataset(dataset,db)
    return db_dataset