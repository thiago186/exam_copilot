"""This file handles the questions routes"""

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
async def create_question_document_on_database(question: QuestionDoc):
    """
    This function receives a question document and creates it on the database.
    """

    try:
        print(f"Received question: {question}")
        await acreate_question(question)
        return {"detail": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("exam/{exam_id}")
async def get_all_exam_questions_by_id(exam_id: str, request: Request):
    """
    Retrieves an exam by id.
    """

    owner_id = get_user_id_from_jwt(request)

    result = await (aget_exam_by_id(exam_id, owner_id))

    return result