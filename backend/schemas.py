from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    DOCX = "docx"
    PPTX = "pptx"


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Project Schemas
class SectionCreate(BaseModel):
    title: str
    order: int


class SectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class SectionResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str
    document_type: DocumentType
    main_topic: str
    sections: List[SectionCreate]


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    main_topic: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    document_type: DocumentType
    main_topic: str
    created_at: datetime
    updated_at: datetime
    sections: List[SectionResponse] = []

    class Config:
        from_attributes = True


# Refinement Schemas
class RefinementRequest(BaseModel):
    prompt: str


class RefinementResponse(BaseModel):
    id: int
    section_id: int
    prompt: str
    previous_content: Optional[str]
    new_content: str
    created_at: datetime

    class Config:
        from_attributes = True


# Feedback Schemas
class FeedbackCreate(BaseModel):
    is_liked: Optional[bool] = None
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    section_id: int
    is_liked: Optional[bool]
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
