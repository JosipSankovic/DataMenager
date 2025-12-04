from pydantic import BaseModel,Field,ConfigDict
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID
from app.schemas import ImageMetadata,LabelAll
class DatasetData(BaseModel):
    train:list[ImageMetadata]= []
    valid:list[ImageMetadata]= []
    test:list[ImageMetadata]= []

class DatasetBase(BaseModel):
    id:UUID
    name:str
    description:str

class DatasetAll(DatasetBase):
    project_id:UUID
    version_id:UUID
    data:DatasetData
    created_at:datetime

class DatasetCreate(BaseModel):
    project_id:UUID
    version_id:UUID
    name:str
    description:str

class LabelDataset(LabelAll):
    rel_path:str
    
# {
#   "images": [
#     {
#       "rel_path": "cat_01.jpg",
#       "image_id": "c13er-fed3f-2131fd-324g-fdswf",
#       "version_id": "fer7-klg3-ber5-3vdw",
#       "path": "s3://bucket/datasets/v1/cat_01.jpg",
#       "augmentations": {
#         "rotation": [90, -90],
#         "brightness": [10, -10],
#         "noise": 5
#       }
#     }
#   ]
# }