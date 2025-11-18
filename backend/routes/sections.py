from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
from ai_service import ai_service

router = APIRouter(prefix="/api/sections", tags=["sections"])


@router.put("/{section_id}", response_model=schemas.SectionResponse)
def update_section(
    section_id: int,
    section_update: schemas.SectionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a section's title or content."""
    
    section = db.query(models.DocumentSection).join(models.Project).filter(
        models.DocumentSection.id == section_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    if section_update.title is not None:
        section.title = section_update.title
    if section_update.content is not None:
        section.content = section_update.content
    
    db.commit()
    db.refresh(section)
    
    return section


@router.post("/{section_id}/refine", response_model=schemas.SectionResponse)
async def refine_section(
    section_id: int,
    refinement: schemas.RefinementRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Refine a section's content using AI based on user prompt."""
    
    section = db.query(models.DocumentSection).join(models.Project).filter(
        models.DocumentSection.id == section_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    if not section.content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Section has no content to refine. Generate content first."
        )
    
    # Store previous content
    previous_content = section.content
    
    # Generate refined content
    refined_content = await ai_service.refine_content(
        current_content=section.content,
        refinement_prompt=refinement.prompt,
        section_title=section.title
    )
    
    # Update section content
    section.content = refined_content
    
    # Create refinement record
    db_refinement = models.Refinement(
        section_id=section.id,
        prompt=refinement.prompt,
        previous_content=previous_content,
        new_content=refined_content
    )
    
    db.add(db_refinement)
    db.commit()
    db.refresh(section)
    
    return section


@router.post("/{section_id}/feedback", response_model=schemas.FeedbackResponse)
def add_feedback(
    section_id: int,
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add feedback (like/dislike/comment) to a section."""
    
    section = db.query(models.DocumentSection).join(models.Project).filter(
        models.DocumentSection.id == section_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    db_feedback = models.Feedback(
        section_id=section.id,
        is_liked=feedback.is_liked,
        comment=feedback.comment
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return db_feedback


@router.get("/{section_id}/refinements", response_model=List[schemas.RefinementResponse])
def get_refinements(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all refinement history for a section."""
    
    section = db.query(models.DocumentSection).join(models.Project).filter(
        models.DocumentSection.id == section_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Section not found"
        )
    
    return section.refinements
