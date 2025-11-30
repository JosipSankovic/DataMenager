from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
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
def create_image(project: ImageCreate, db: Session = Depends(get_db))->ImageBase:
    db_image = images_service.create_image(project,db)
    return db_image

@router.post("/add_imgs_to_project",response_model=list[ImageBase])
def add_img_to_project(imgs_dir:str,images:list[str],project_id:str,
                    db: Session = Depends(get_db))->list[ImageBase]:
    db_images = images_service.create_image_batch(imgs_dir,images,project_id,db)
    return db_images
@router.get("/folder_images")
def get_folder_images(folder_path:str,page:int,db:Session = Depends(get_db))->list[str]:
    folder_images = images_service.get_folder_images(folder_path,page,db)
    return folder_images

@router.get("/serve_image")
def serve_file(file_path: str):
    # Ovdje backend čita sliku s diska i šalje je frontend-u
    import os
    if not os.path.exists(file_path):
        print("File dont exists")
        raise HTTPException(status_code=404,detail="File dont exist")
    return FileResponse(file_path)