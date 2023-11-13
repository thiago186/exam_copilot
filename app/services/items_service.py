"""
Items services for upload and create items in the database
"""

import json
import logging

from schemas.items import ImageDoc, QuestionDoc
from connectors.firebase_connector import aupload_image
from connectors.mongodb_connector import acreate_image_doc, ainsert_document, aquery_items
from schemas.items import CollectionsTypes


async def aupload_and_create_image(image_doc: ImageDoc) -> None:
    """
    Uploads an image to Firebase and creates an image document in MongoDB
    """
    image_doc = await aupload_image(image_doc)
    logging.debug(f"image_doc: {image_doc}")
    await acreate_image_doc(image_doc)


async def acreate_question(question: QuestionDoc) -> None:
    """
    Creates a question document in MongoDB
    """

    json_question = json.loads(question.json())
    await ainsert_document(json_question, CollectionsTypes.QUESTIONS)


async def aget_exam_by_id(exam_id: str, owner_id: str) -> list:
    """
    Retrieves an exam by id. The expected return is a list of all questions.
    """

    query = {
        "exam_id": exam_id,
        "owner_id": owner_id
    }

    logging.debug(f"passing query `{query}` for aquery_items functions on collection {CollectionsTypes.QUESTIONS}")
    result = await (aquery_items(query, CollectionsTypes.QUESTIONS))

    return result
