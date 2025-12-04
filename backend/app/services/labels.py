import os
import numpy as np
import shutil
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import insert, desc, update,and_
from app.schemas import LabelBase, LabelCreate, LabelUpdate, ImageBase
from app.models import Label
import sys
from app.utils import DataTracker


class LabelsService:

    def get_image_label(
        self,image_id: str, db: Session, version_id: str = None
    ) -> LabelBase|None:
        filter_query = None
        if version_id:
            filter_query =db.query(Label).filter(and_(Label.image_id==image_id,Label.version_id==version_id))
        else:
            filter_query =db.query(Label).filter(Label.image_id==image_id)

        db_label = (
            filter_query
            .distinct(Label.image_id)
            .order_by(Label.image_id, desc(Label.created_at))
            .first()
        )
        return db_label

    def get_version_labels(
        self,
        version_id: str,
        project_id: str,
        db: Session,
        use_not_finished=True,
        offset=0,
        limit=sys.maxsize,
    ) -> list[LabelBase]:
        labels = []
        from app.models import Images

        base_query = (
            db.query(Label)
            .join(Images, Label.image_id == Images.id)
            .filter(Images.project_id == project_id)
        )
        if use_not_finished:
            labels = (
                base_query.filter(
                    (Label.version_id == version_id) | (Label.version_id == None)
                )
                .distinct(Label.image_id)
                .order_by(Label.image_id, desc(Label.created_at))
                .offset(offset)
                .limit(limit)
                .all()
            )
        else:
            labels = (
                base_query.filter(Label.version_id == version_id)
                .distinct(Label.image_id)
                .order_by(Label.image_id, desc(Label.created_at))
                .offset(offset)
                .limit(limit)
                .all()
            )
        return labels

    def get_latest_labels(self, project_id: str, db: Session) -> list[LabelBase]:
        labels = []
        from app.models import Images

        base_query = (
            db.query(Label)
            .join(Images, Label.image_id == Images.id)
            .filter(Images.project_id == project_id)
        )
        labels = (
            base_query.distinct(Label.image_id)
            .order_by(Label.image_id, desc(Label.created_at))
            .all()
        )

        return labels

    def get_unversion_labels(
        self,
        project_id: str,
        db: Session,
    ) -> list[LabelBase]:
        labels = []
        from app.models import Images

        base_query = (
            db.query(Label)
            .join(Images, Label.image_id == Images.id)
            .filter(Images.project_id == project_id)
        )
        labels = (
            base_query.filter((Label.version_id == None))
            .distinct(Label.image_id)
            .order_by(Label.image_id, desc(Label.created_at))
            .all()
        )
        return labels

    def add_label(self, label: LabelCreate, db: Session) -> LabelBase:
        db_label = Label(
            image_id=label.image_id, version_id=label.version_id, data=label.data
        )
        db.add(db_label)
        db.commit()
        return db_label

    def add_labels_batch_from_images(
        self, project_path: str, images: list[ImageBase], db: Session
    ) -> list[LabelBase]:
        if len(images) == 0:
            return []
        created_labels = []
        now = datetime.now(timezone.utc)

        for image in images:
            full_path = os.path.join(project_path, image["rel_path"])
            json_data, label_path = DataTracker.get_labels_data(full_path)
            if json_data is None:
                continue
            created_labels.append(
                {
                    "id": uuid.uuid4(),
                    "image_id": image["id"],
                    "version_id": None,
                    "data": json_data,
                    "created_at": now,
                }
            )
        return self.add_labels_batch(created_labels, db)

    def add_labels_batch(
        self, labels: list[LabelCreate], db: Session
    ) -> list[LabelBase]:
        if len(labels) == 0:
            return []
        stmt = insert(Label).values(labels)
        db.execute(stmt)
        db.commit()
        return labels

    def update_labels_batch(
        self, updated_labels: list[LabelUpdate], db: Session
    ) -> None:
        if len(updated_labels) == 0:
            return []
        db.execute(update(Label), updated_labels)
        db.commit()
        return None

    def apply_version(self, version_id: str, project_id: str, db: Session) -> dict:
        unversioned_labels = self.get_unversion_labels(project_id, db)
        label_ids = [label.id for label in unversioned_labels]

        stmt = (
            update(Label).where(Label.id.in_(label_ids)).values(version_id=version_id)
        )
        result = db.execute(stmt)
        # Ovo sprema sve promjene u bazu
        db.commit()
        return {"updated_count": result.rowcount}

    