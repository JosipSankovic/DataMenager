from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ProjectBase, ProjectCreate
from app.models import Project
from app.services import ProjectService
from app.core import get_db  # Correctly import get_db from database module

router = APIRouter(prefix="/projects", tags=["projects"])

project_service = ProjectService()
@router.post("/", response_model=ProjectBase)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    # Create the ORM object
    db_project = project_service.create_project(project, db)
    return db_project


@router.get("/", response_model=list[ProjectBase])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Query using SQLAlchemy
    projects = project_service.get_projects(skip,limit,db)
    return projects

@router.get("/{project_id}",response_model = ProjectBase)
def get_project(project_id:str,db:Session=Depends(get_db))->ProjectBase:
    project = project_service.get_project(project_id,db)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", response_model=ProjectBase)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = project_service.get_project(project_id,db)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return project
