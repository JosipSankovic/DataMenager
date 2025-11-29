from app.models import Project
from app.schemas import ProjectBase, ProjectCreate
from sqlalchemy.orm import Session
import os
def sanitaze_path(path:str)->str:
    return os.path.normpath(path)
class ProjectService:
    def create_project(self,project_to_create: ProjectCreate, db:Session)->ProjectBase:


        db_project = Project(
            name= project_to_create.name,
            description = project_to_create.description,
            absolute_path=sanitaze_path(project_to_create.absolute_path)
        )
        db.add(db_project)
        db.commit()
        return db_project

    def get_project(self,project_id:int,db:Session)->ProjectBase|None:
        db_project=db.query(Project).filter(Project.id==project_id).first()
        return db_project
    
    def get_projects(self,offset:int, limit:int,db:Session)->list[ProjectBase]:
        projects = db.query(Project).offset(offset).limit(limit).all()
        return projects