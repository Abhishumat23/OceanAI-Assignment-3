from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import get_current_user
from document_service import document_exporter

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/{project_id}")
async def export_document(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Export a project as .docx or .pptx file."""
    
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all sections
    sections = db.query(models.DocumentSection).filter(
        models.DocumentSection.project_id == project.id
    ).all()
    
    if not sections:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project has no sections to export"
        )
    
    # Export based on document type
    if project.document_type == models.DocumentType.DOCX:
        file_bytes = document_exporter.export_docx(project, sections)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"{project.title}.docx"
    else:  # PPTX
        file_bytes = document_exporter.export_pptx(project, sections)
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        filename = f"{project.title}.pptx"
    
    # Clean filename
    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
    
    return Response(
        content=file_bytes,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
