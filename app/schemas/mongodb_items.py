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
    owner_id: UUID = Field(default_factory=uuid4)


class ImageDoc(BaseDoc, use_enum_values=True):
    """Image document schema."""

    name: str
    path: str
    exam_id: Optional[UUID] = uuid4()
    student_label: str
    question: int
    page: int
    total_pages: int


class ExamTypes(str, Enum):
    """
    Existing exam types.
    This code has not been tested yet.
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
    exam_id: Optional[uuid4] = Field(default_factory=uuid4)
    exam_type: ExamTypes
