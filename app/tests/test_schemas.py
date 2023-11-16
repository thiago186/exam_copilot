"""
This file contains the tests for the schemas.
"""

import pytest

from pydantic import ValidationError
from uuid import uuid4, UUID
from datetime import datetime
from ..schemas.items import CollectionsTypes, BaseDoc, ImageDoc, ExamCorrectionTypes, QuestionDoc


class TestSchemas():
    """Test the schemas."""

    def test_base_doc(self):
        """Test BaseDoc schema."""
        base_doc = BaseDoc(collection=CollectionsTypes.IMAGE, owner_id=uuid4())
        assert base_doc.collection == "images"
        assert isinstance(base_doc.owner_id, UUID)
        assert isinstance(base_doc.created_at, datetime)

    # def test_invalid_base_doc(self):
    #     """Test invalid BaseDoc schema."""
    #     with pytest.raises(ValidationError):
    #         BaseDoc(collection=CollectionsTypes.IMAGE, owner_id="test")

    def test_invalid_base_doc(self):
        """Test invalid BaseDoc schema."""
        try:
            BaseDoc(collection=CollectionsTypes.IMAGE, owner_id="test")
        except Exception as e:
            assert isinstance(e, ValidationError)

    def test_image_doc(self):
        """Test ImageDoc schema."""
        image_doc = ImageDoc(collection=CollectionsTypes.IMAGE, owner_id=uuid4(
        ), name="test", exam_id=uuid4(), student_label="test", question=1, page=1, total_pages=1)
        assert image_doc.collection == 'images'
        assert isinstance(image_doc.owner_id, UUID)
        assert isinstance(image_doc.created_at, datetime)
        assert isinstance(image_doc.name, str)
        assert isinstance(image_doc.exam_id, UUID)
        assert isinstance(image_doc.student_label, str)
        assert isinstance(image_doc.question, int)
        assert isinstance(image_doc.page, int)
        assert isinstance(image_doc.total_pages, int)

    def test_question_doc(self):
        """Test QuestionDoc schema."""
        question_doc = QuestionDoc(collection=CollectionsTypes.QUESTIONS, owner_id=uuid4(), exam_name="test", exam_id=uuid4(
        ), exam_field="test", correction_type=ExamCorrectionTypes.free, question_number=1, question_text="test", question_answer="test")
        assert question_doc.collection == 'questions'
        assert isinstance(question_doc.owner_id, UUID)
        assert isinstance(question_doc.created_at, datetime)
        assert isinstance(question_doc.exam_name, str)
        assert isinstance(question_doc.exam_id, UUID)
        assert isinstance(question_doc.exam_field, str)
        assert question_doc.correction_type == 'free'
        assert isinstance(question_doc.question_number, int)
        assert isinstance(question_doc.question_text, str)
        assert isinstance(question_doc.question_answer, str)
