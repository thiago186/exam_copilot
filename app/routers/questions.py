"""This file handles the questions routes"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Request

from config import settings
from routers.router_utils import validate_token, get_user_id_from_jwt
from schemas.items import CollectionsTypes, QuestionDoc
from services.items_service import acreate_question, aget_exam_by_id



router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    dependencies=[Depends(validate_token)],
)

@router.post("")
async def create_question_document_on_database(question: QuestionDoc, request: Request):
    """
    This function receives a question document and creates it on the database.
    """

    try:
        question.owner_id = get_user_id_from_jwt(request)
        await acreate_question(question)
        return {"detail": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("exam/{exam_id}")
async def get_all_exam_questions_by_id(exam_id: str, request: Request):
    """
    Retrieves an exam by id.
    """

    logging.debug("getting exam by id")
    owner_id = get_user_id_from_jwt(request)

    logging.debug("owner id retrieved succesfully, getting exam from database")
    exam_questions = await aget_exam_by_id(exam_id, owner_id)
    logging.debug(f"exam retrieved succesfully: {exam_questions} | type: {type(exam_questions)}")

    return {"exam": exam_questions}