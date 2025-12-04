from app.schemas import DatasetAll,DatasetBase,DatasetData,DatasetCreate
from sqlalchemy.orm import Session
from app.models import Dataset,Label,Version,Images
from app.schemas import LabelBase, LabelCreate, LabelUpdate, ImageBase,LabelAll,LabelDataset,ImageMetadata
from sqlalchemy import desc
import uuid
class DatasetService:
    
    def get_all_datasets(self,project_id:str,db:Session)->list[DatasetBase]:
        db_datasets=db.query(Dataset).filter(Dataset.project_id==project_id).all()
        return db_datasets
    
    def create_dataset(self,dataset:DatasetCreate,db:Session)->DatasetBase:
        db_dataset = Dataset(
            project_id=dataset.project_id,
            version_id=dataset.version_id,
            name = dataset.name,
            description = dataset.description,
        )

        db.add(db_dataset)
        db.commit()
        return db_dataset


    def create_automatic_dataset(self,db:Session,dataset:DatasetCreate,train:float=0.7,
                                 valid:float=0.2)->list[DatasetAll]:
        # get all images with latest labels before and with version_id
        # split them into train,valid,test
        # create json with all images that are selected and their augmentation settings
        # put it in database 
        # autgment all images inside train
        from sklearn.model_selection import train_test_split
        import random
        random.seed(42)


        all_labels,rarest_labels=self.get_labels_for_dataset(dataset.project_id,dataset.version_id,db)
        if len(all_labels)<10:
            raise ValueError("Size of dataset is too small")
        train_data,temp_data,data_labels,temp_labels = train_test_split(all_labels,rarest_labels,test_size=(1.0-train),stratify=rarest_labels,random_state=42)
        if len(temp_data) > 0:
            relative_valid_size = min(0.999, valid / (1.0 - train))
        else:
            relative_valid_size = 0.5 # Fallback ako nema podataka

        valid_data, test_data= train_test_split(
        temp_data, test_size=(1.0 - relative_valid_size), stratify=temp_labels, random_state=42)
       

        train_dataset:list[ImageMetadata] = populate_dataset(train_data)
        valid_dataset:list[ImageMetadata] = populate_dataset(valid_data)
        test_dataset:list[ImageMetadata] = populate_dataset(test_data)
        d_data = DatasetData(
            train=train_dataset,
            valid=valid_dataset,
            test=test_dataset
        )
        db_dataset = Dataset(
            project_id=dataset.project_id,
            version_id=dataset.version_id,
            description=dataset.description,
            name=dataset.name,
            data=d_data
        )
        db.add(db_dataset)
        db.commit()
        return db_dataset
    def get_labels_for_dataset(self,project_id:str,version_id:str,db:Session)->(list[LabelDataset],list[str]):
        from collections import Counter
        target_version_date=db.query(Version.created_at).filter(Version.id==version_id).scalar()

        if not target_version_date:
            raise ValueError("Version ID not found")
        
        results = (
                 db.query(Label,Images.rel_path)
                .join(Images,Label.image_id==Images.id)
                .join(Version,Label.version_id==Version.id)
                .filter(
                    Images.project_id==project_id,
                    Version.created_at<=target_version_date,
                )
                .distinct(Label.image_id)
                .order_by(
                    Label.image_id,
                    desc(Version.created_at)
                ).all()
        )
        print("returned all labels")
        labels = []
        rarest_labels = []
        class_counter =Counter()
        # first get number of all labels in dataset
        for label_obj,path_str in results:
            #get all labels in image
            if not label_obj.data:
               continue
            shapes_list = label_obj.data.get("shapes", [])
            current_image_labels = [s["label"] for s in shapes_list]
            if not current_image_labels:
                continue
            class_counter.update(current_image_labels)
            labels.append(
                LabelDataset(
            id=label_obj.id,
            image_id=label_obj.image_id,
            version_id=label_obj.version_id,
            data=label_obj.data,
            created_at=label_obj.created_at,
            rel_path=path_str)
            )
            
        for label_obj,path_str in results:
            if not label_obj.data:
                continue
            shapes_list = label_obj.data.get("shapes", [])
            current_image_labels = [s["label"] for s in shapes_list]
            if not current_image_labels:
                # Slučaj kad slika nema anotacija
                continue
            else:
                rarest = min(current_image_labels, key=lambda x: class_counter[x])
                rarest_labels.append(rarest)
        return labels,rarest_labels
def populate_dataset(all_labels:list[LabelDataset])->list[ImageMetadata]:
    return [
            ImageMetadata(
                image_id=label.image_id,
                version_id=label.version_id,
                rel_path=label.rel_path,
                augmentations={
                    "rotation":[90.0,-90.0],
                    "brightness": [10.0, -10.0]
                }
            )
            for label in all_labels
        ]