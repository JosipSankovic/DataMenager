from fastapi import HTTPException
from app.schemas import DatasetAll,DatasetBase,DatasetData,DatasetCreate
from sqlalchemy.orm import Session
from app.models import Dataset,Label,Version,Images
from app.schemas import LabelBase, LabelCreate, LabelUpdate, ImageBase,LabelAll,LabelDataset,ImageMetadata,ProjectBase
from app.services import LabelsService,ProjectService
from sqlalchemy import desc
import uuid
import os

# This tells Windows: "Look in this folder for the missing DLLs"
os.add_dll_directory(r"E:\Programs\vcpkg\installed\x64-windows\bin")
label_service = LabelsService()
project_service = ProjectService()
import fast_augmentation
class DatasetService:
    
    def get_dataset(self,dataset_id:str,db:Session)->DatasetAll|None:
        dataset=db.query(Dataset).where(Dataset.id==dataset_id).first()
        return dataset

    def get_all_datasets(self,project_id:str,db:Session)->list[DatasetBase]:
        db_datasets=db.query(Dataset).filter(Dataset.project_id==project_id).all()
        return db_datasets
    
    def create_dataset(self,dataset_id:str,db:Session)->DatasetBase:
        import json
        dataset:DatasetAll=self.get_dataset(dataset_id,db)
        if dataset is None:
            raise HTTPException(404,"No dataset with that id")
        project:ProjectBase= project_service.get_project(dataset.project_id,db)
        if project is None:
            raise HTTPException(404,"No project for this dataset")
        data:DatasetData = dataset.data
        version_id = dataset.version_id
        send_size = 0
        LIMIT = 5000
        data_list = []
        image_ids =[]
        for image in data["train"]:
            image_id =image["image_id"]
            image_ids.append(image_id)
        img_lbl_dict=label_service.get_batch_image_label(image_ids,version_id,db)
        for image in data["train"]:
            data_list.append((json.dumps(image),json.dumps(img_lbl_dict[image["image_id"]])))
        label_names = ["fish","tail"]
        project_root = project.absolute_path
        dataset_new_path = os.path.join(project_root,dataset.name)
        os.makedirs(name=dataset_new_path,exist_ok=True)
        fast_augmentation.process_json(data_list,project_root,dataset_new_path,label_names)
        # db.add(db_dataset)
        # db.commit()
        return None

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
            size = len(all_labels),
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
                    "rotation":[90.0,-90.0,45.0,-210.0],
                    "brightness": [10.0, -10.0,100,-100,1000]
                }
            )
            for label in all_labels
        ]