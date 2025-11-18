from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class DocumentType(str, enum.Enum):
    DOCX = "docx"
    PPTX = "pptx"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    main_topic = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="projects")
    sections = relationship("DocumentSection", back_populates="project", cascade="all, delete-orphan")


class DocumentSection(Base):
    __tablename__ = "document_sections"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="sections")
    refinements = relationship("Refinement", back_populates="section", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="section", cascade="all, delete-orphan")


class Refinement(Base):
    __tablename__ = "refinements"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("document_sections.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    previous_content = Column(Text, nullable=True)
    new_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    section = relationship("DocumentSection", back_populates="refinements")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("document_sections.id"), nullable=False)
    is_liked = Column(Boolean, nullable=True)  # True for like, False for dislike, None for no feedback
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    section = relationship("DocumentSection", back_populates="feedback")
