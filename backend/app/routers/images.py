from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import ImagesService
from app.schemas import ImageBase, ImageCreate
from app.core import get_db
router = APIRouter(prefix="/images",tags=["images"])

images_service = ImagesService()

@router.get("/",response_model=list[ImageBase])
def get_all(project_id:str,skip: int = 0, limit: int = 100,db:Session = Depends(get_db))->list[ImageBase]:
    images = images_service.get_images(project_id,db,skip,limit)
    return images

@router.post("/", response_model=ImageBase)
def create_project(project: ImageCreate, db: Session = Depends(get_db))->ImageBase:
    db_image = images_service.create_image(project,db)
    return db_image


@router.get("/folder_images")
def get_folder_images(folder_path:str,page:int,db:Session = Depends(get_db))->list[str]:
    folder_images = images_service.get_folder_images(folder_path,page,db)
    return folder_images