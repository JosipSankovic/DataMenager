from app.models import Images
from sqlalchemy.orm import Session
from sqlalchemy import insert
from app.schemas import ImageBase, ImageCreate
import os
from fastapi import HTTPException
import cv2
import numpy as np
import shutil
import uuid
from datetime import datetime,timezone


class ImagesService:

    def get_images(
        self, project_id: str, db: Session, offset=0, limit=100
    ) -> list[ImageBase]:
        images = (
            db.query(Images)
            .filter(Images.project_id == project_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return images

    def create_image(self, image: ImageCreate, db: Session) -> ImageBase:
        db_image = Images(
            project_id=image.project_id,
            rel_path=image.rel_path,
            width=image.width,
            height=image.height,
            channels=image.channels,
            mime_type=image.mime_type,
            is_annotated=image.is_annotated,
        )
        db.add(db_image)
        db.commit()
        return db_image

    def create_image_batch(self,imgs_dir:str,images:list[str],project_id:str,db:Session)->list[ImageBase]:
        from app.services import ProjectService
        from app.schemas import ProjectBase
        project_service =ProjectService()
        project:ProjectBase|None = project_service.get_project(project_id,db)
        if project is None:
            raise HTTPException(status_code=404, detail="Cant find project")
        project_path = project.absolute_path
        img_objects: list[ImageCreate] = []

        for img_name in images:
            from_img_path=os.path.join(imgs_dir,img_name)
            to_img_path=os.path.join(project_path,img_name)

            if not os.path.exists(from_img_path):
                continue
            stream = np.fromfile(from_img_path, dtype=np.uint8)
            img = cv2.imdecode(stream, cv2.IMREAD_COLOR)
            if img is None:
                continue
            height,width,channels = img.shape
            extension = img_name.split(".")[-1].lower()
            shutil.move(from_img_path,to_img_path)
            if not os.path.exists(to_img_path):
                continue
            print(img_name)
            project_id_uuid = None
            if isinstance(project_id, str):
                project_id_uuid = uuid.UUID(project_id)
            else:
                project_id_uuid = project_id
            new_id = uuid.uuid4()
            now = datetime.now(timezone.utc)
            img_objects.append({
            "id": uuid.uuid4(),  # Generiramo UUID objekt
            "project_id": project_id_uuid,
            "rel_path": img_name,
            "width": width,
            "height": height,
            "channels": channels,
            "mime_type": f"image/{extension}",
            "is_annotated": False,
            "created_at": now})
        
        stmt = insert(Images).values(img_objects)
        db.execute(stmt)
        db.commit()
        return img_objects

        
    def get_folder_images(self, folder_path: str, page: int, db: Session,page_size = 150) -> list[str]:
        if page <= 0:
            page = 1
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404,detail="Folder doesnt exist")
        idx = 0
        folder_images = []
        for image in sorted(os.listdir(folder_path), key=str.lower):
            if not image.lower().endswith(("jpg", "jpeg", "png")):
                continue
            idx += 1

            if idx >= (page - 1) * page_size and idx < page * page_size:
                folder_images.append(image)
        return folder_images
