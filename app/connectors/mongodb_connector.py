""" Contains the connectors for interacting with items inside 
the mongodb database. 
"""
import json
from uuid import UUID
import logging

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config import settings
from schemas.items import CollectionsTypes, ImageDoc

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

async def aquery_items(query: dict, collection: CollectionsTypes):
    """This function retrieves items based on a query dict."""

    collection = db[collection.value]

    logging.debug(f"executing query: {query} on collection `{collection}`")
    result = collection.find(query)

    return result