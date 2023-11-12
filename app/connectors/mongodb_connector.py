""" Contains the connectors for interacting with items inside 
the mongodb database. 
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import settings
from app.schemas.items import CollectionsTypes, ExamDoc, ImageDoc

connection_string = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}"

client = MongoClient(connection_string, server_api=ServerApi("1"))

db = client[settings.MONGO_DB]

async def acreate_image(image: ImageDoc):
    """Creates a new image document on the database."""
    collection = db[CollectionsTypes.IMAGE.value]

    result = collection.insert_one(image.dict())

    return result.inserted_id

async def acreate_exam(exam: ExamDoc):
    """Creates a new exam document on the database."""
    collection = db[CollectionsTypes.EXAM.value]

    result = collection.insert_one(exam.dict())

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