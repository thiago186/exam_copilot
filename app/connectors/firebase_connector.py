"""These file contains the firebase bucket connector"""

import json
import logging
from uuid import uuid4

import firebase_admin
from firebase_admin import storage, credentials

from config import settings
from schemas.items import ImageDoc


credentials = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILENAME)

firebase_admin.initialize_app(
    credentials, {"storageBucket": settings.FIREBASE_BUCKET_URL}
)  # connecting to firebase


async def aupload_image(image: ImageDoc):
    """Uploads an image to the firebase bucket"""
    img_name, img_extension = image.name.split(".")
    new_name = f"{img_name}-{uuid4()}.{img_extension}"
    blob_filename = f"{image.collection}/{new_name}"
    image_path = f"{settings.LOCAL_MEDIA_PATH}/{image.name}"

    bucket = storage.bucket()
    blob = bucket.blob(blob_filename)
    blob.upload_from_filename(image_path)
    blob.metadata = json.loads(image.json())

    image.url = blob.public_url
    image.name=new_name

    logging.info(f"Image uploaded to firebase: {image.name}")
    return image

