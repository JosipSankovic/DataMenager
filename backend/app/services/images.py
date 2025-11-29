from app.models import Images
from sqlalchemy.orm import Session
from app.schemas import ImageBase, ImageCreate
import os
from fastapi import HTTPException

PAGE_SIZE = 5


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

    def get_folder_images(self, folder_path: str, page: int, db: Session) -> list[str]:
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

            if idx >= (page - 1) * PAGE_SIZE and idx < page * PAGE_SIZE:
                folder_images.append(image)
        return folder_images
