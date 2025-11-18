from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
from ai_service import ai_service

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new project with sections."""
    
    # Create project
    db_project = models.Project(
        title=project.title,
        document_type=project.document_type,
        main_topic=project.main_topic,
        user_id=current_user.id
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Create sections
    for section in project.sections:
        db_section = models.DocumentSection(
            project_id=db_project.id,
            title=section.title,
            order=section.order,
            content=None  # Content will be generated later
        )
        db.add(db_section)
    
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.get("", response_model=List[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all projects for the current user."""
    
    projects = db.query(models.Project).filter(
        models.Project.user_id == current_user.id
    ).all()
    
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a specific project by ID."""
    
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a project."""
    
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project_update.title is not None:
        project.title = project_update.title
    if project_update.main_topic is not None:
        project.main_topic = project_update.main_topic
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a project."""
    
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return None


@router.post("/{project_id}/generate", response_model=schemas.ProjectResponse)
async def generate_content(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generate AI content for all sections in the project."""
    
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Generate content for each section
    for section in project.sections:
        if not section.content:  # Only generate if content doesn't exist
            content = await ai_service.generate_section_content(
                topic=project.main_topic,
                section_title=section.title,
                document_type=project.document_type.value
            )
            section.content = content
    
    db.commit()
    db.refresh(project)
    
    return project
