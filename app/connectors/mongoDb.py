from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import settings

connection_string = f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}"

client = MongoClient(connection_string, server_api=ServerApi("1"))

db = client[settings.MONGO_DB]
collection = db["images"]

mockDocument = {
    "name": "image_name",
    "path": "path/to/image/",
    "exam_id": "mockExamUuid",
    "owner_id": "OwnerUserId",
    "page": 1,
}

result = collection.insert_one(mockDocument)