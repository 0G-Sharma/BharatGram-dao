from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
from services.algorand_service import algo_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/by_village/{village_id}", response_model=list[schemas.ProjectResponse])
def projects_by_village(village_id: int, db: Session = Depends(get_db)):
    return crud.get_projects_by_village(db, village_id)


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/add", response_model=schemas.ProjectResponse)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = crud.create_project(db, payload)
    # Sync to Blockchain
    try:
        project_data = {"name": project.name, "budget": project.budget}
        algo_service.sync_project(project.id, int(project.budget), int(project.spent), project_data, is_new=True)
    except Exception as e:
        print(f"Blockchain Sync Error: {e}")
    return project


@router.put("/update/{project_id}", response_model=schemas.ProjectResponse)
def update_project(project_id: int, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = crud.update_project(db, project_id, payload)
    # Sync to Blockchain
    if project:
        try:
            project_data = {"name": project.name, "budget": project.budget, "status": project.status}
            algo_service.sync_project(project.id, int(project.budget), int(project.spent), project_data, is_new=False)
        except Exception as e:
            print(f"Blockchain Sync Error: {e}")
    return project

@router.get("/verify/{project_id}")
def verify_project_on_chain(project_id: int):
    data = algo_service.get_on_chain_data(project_id)
    if not data:
        raise HTTPException(status_code=404, detail="Project not found on blockchain")
    return data


@router.delete("/delete/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return crud.delete_project(db, project_id)
