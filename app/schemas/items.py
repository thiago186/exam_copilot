"""
This file contains the schemas used for the files
on database and storage bucket.
"""

from datetime import datetime
import logging
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, root_validator, Field
from enum import Enum


class CollectionsTypes(str, Enum):
    """Existing collections on the database."""

    IMAGE = "images"
    EXAM = "exams"
    QUESTIONS = "questions"


class BaseDoc(BaseModel, use_enum_values=True):
    """Base document schema."""

    collection: CollectionsTypes
    owner_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ImageDoc(BaseDoc, use_enum_values=True):
    """Image document schema."""

    name: str
    path: Optional[str] = ""
    exam_id: UUID
    student_label: str
    question: int
    page: int
    total_pages: int


class ExamTypes(str, Enum):
    """
    Existing exam types.
    """

    free = "free"  # free correction
    BINARY = "binary"  # binary correction
    INSTRUCTED = "instructed"  # instructed correction


class ExamDoc(BaseModel, use_enum_values=True):
    """
    Exam document schema.
    This code has not been tested yet.
    """

    exam_name: str
    exam_id: Optional[UUID] = Field(default_factory=uuid4)
    exam_type: ExamTypes
