""" Contains the connectors for interacting with items inside 
the mongodb database. 
"""
import json

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import settings
from schemas.items import CollectionsTypes, ExamDoc, ImageDoc

connection_string = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}"

client = MongoClient(connection_string, server_api=ServerApi("1"))

db = client[settings.MONGO_DB]

async def ainsert_document(document: dict, collection: CollectionsTypes):
    """Inserts a document on the database."""

    collection = db[collection.value]

    result = collection.insert_one(document)

    return result.inserted_id

async def acreate_image_doc(image: ImageDoc):
    """Creates a new image document on the database."""
    
    img_json = json.loads(image.json())
    collection = db[CollectionsTypes.IMAGE.value]

    result = collection.insert_one(img_json)

    return result.inserted_id

async def acreate_exam_doc(exam: ExamDoc):
    """Creates a new exam document on the database."""

    doc_json = json.loads(exam.json())
    collection = db[CollectionsTypes.EXAM.value]

    result = collection.insert_one(doc_json)

    return result.inserted_id

# collection = db["images"]

# mockDocument = {
#     "name": "image_name",
#     "path": "path/to/image/",
#     "exam_id": "mockExamUuid",
#     "owner_id": "OwnerUserId",
#     "page": 1,
# }

# result = collection.insert_one(mockDocument)