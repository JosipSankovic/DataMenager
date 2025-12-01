from app.schemas import ImageBase,ImageIds,LabelBase
import os
import json
import uuid
from datetime import datetime,timezone

def check_untracked(folder_path:str,db_images:list[ImageIds],db_labels:list[LabelBase]):

    existing_labels_map={str(label.image_id):label for label in db_labels}
    not_versioned_labels = []
    updated_labels = []
    deleted_labels = []
    deleted_images:list[uuid.UUID] = []
    now = datetime.now(timezone.utc)
    imgs_in_dir = {str(img):img for img in os.listdir(folder_path) if img.lower().endswith(("jpg","png","jpeg"))}
    
    for img in db_images:
        img_abs_path=os.path.join(folder_path,img.rel_path)
        db_existing_label = existing_labels_map.get(str(img.id))
        # if deleted from main folder delete from db
        if not os.path.exists(img_abs_path):
            deleted_images.append({
                "id":img.id})
            continue
        json_data,label_name = get_labels_data(img_abs_path)
        if imgs_in_dir.get(img.rel_path):
            imgs_in_dir.pop(img.rel_path)
        

        # if json_data is None:
        #     continue
        # if not in db
        if db_existing_label is None:
            not_versioned_labels.append({
                    "id":uuid.uuid4(),
                    "image_id": img.id,
                    "version_id": None,
                    "data": json_data,
                    "created_at":now
            }
            )
            continue
        # if it is in db check for differences with 
        # current file

        #same
        if db_existing_label.data == json_data:
            continue
        ## changed label
        # if version_id is None then update label data in db
        # if version_id is not none then create new label in db
        if db_existing_label.version_id:
            not_versioned_labels.append({
                    "id":uuid.uuid4(),
                    "image_id": img.id,
                    "version_id": None,
                    "data": json_data,
                    "created_at":now
            }
            )
            continue
        else:
            updated_labels.append({
                "id":db_existing_label.id,
                "version_id":db_existing_label.version_id,
                "data":json_data
            })
    new_imgs = [data[0] for data in imgs_in_dir.items()]
    return not_versioned_labels,updated_labels,deleted_images,new_imgs







def get_labels_data(img_path: str):
    base_name, _ = os.path.splitext(img_path)
    label_name = f"{base_name}.json"
    
    if os.path.exists(label_name):
        try:
            with open(label_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                return (data,label_name)
        except Exception as e:
            print(f"Greška pri čitanju JSON-a {label_name}: {e}")
            return (None,label_name)
    return (None,label_name)