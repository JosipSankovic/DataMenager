import os
import numpy as np
import shutil
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from sqlalchemy import insert, desc, update,and_
from app.schemas import LabelBase, LabelCreate, LabelUpdate, ImageBase,LabelAll
from app.models import Label, Version
import sys
from app.utils import DataTracker

class LabelsService:

    def get_image_label(
        self, image_id: str, db: Session, version_id: str = None
    ) -> LabelBase | None:
        
        query = db.query(Label).join(Version, Label.version_id == Version.id).filter(Label.image_id == image_id)

        if version_id:
            target_version = db.query(Version).filter(Version.id == version_id).first()
            if target_version:
                query = query.filter(Version.created_at <= target_version.created_at)
        result = (
            query
            .order_by(desc(Version.created_at))
            .first()
        )
        return result
    # provjerit
    def get_batch_image_label(
            self,image_ids:list[str],version_id:str,db:Session
    )->dict[str,LabelAll]:
        """
        Returns a dictionary mapping {image_id: LabelObject}
        Efficiently fetches the 'closest prior' label for a batch of images.
        """
        
        # 1. Determine the cutoff timestamp (1 Query)
        cutoff_date = None
        if version_id:
            target_ver = db.query(Version.created_at).filter(Version.id == version_id).scalar()
            if target_ver:
                cutoff_date = target_ver
        
        # 2. Build the Main Query
        # We want to filter by the list of images and the date cutoff
        query = db.query(Label).join(Version, Label.version_id == Version.id)
        
        query = query.filter(Label.image_id.in_(image_ids))
        
        if cutoff_date:
            query = query.filter(Version.created_at <= cutoff_date)

        # --- STRATEGY SELECTION ---
        
        # OPTION A: If you are using PostgreSQL (Best/Fastest)
        # Postgres has a special feature called DISTINCT ON that solves this perfectly.
        # It keeps only the first row for each image_id, based on the order_by.
        """
        labels = (
            query
            .distinct(Label.image_id)
            .order_by(Label.image_id, desc(Version.created_at))
            .all()
        )
        """

        # OPTION B: Generic SQL (SQLite, MySQL, Postgres compatible)
        # If you aren't strictly on Postgres, we use a Subquery + Row Number.
        # We assign a 'rank' to every label per image, ordered by date.
        
        subquery = (
            db.query(
                Label.id.label("label_id"),
                Label.image_id,
                func.row_number().over(
                    partition_by=Label.image_id,
                    order_by=desc(Version.created_at)
                ).label("rank")
            )
            .join(Version, Label.version_id == Version.id)
            .filter(Label.image_id.in_(image_ids))
        )

        if cutoff_date:
            subquery = subquery.filter(Version.created_at <= cutoff_date)

        subquery = subquery.subquery()

        # Now we select the actual Label objects where rank == 1
        # We join the original Label table against our ranked subquery
        labels = (
            db.query(Label)
            .join(subquery, Label.id == subquery.c.label_id)
            .filter(subquery.c.rank == 1)
            .all()
        )

        # 3. Convert list to dictionary for O(1) lookups
        return {str(label.image_id): label.data for label in labels}
        
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

    