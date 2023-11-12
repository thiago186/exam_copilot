"""
Items services for upload and create items in the database
"""

from schemas.items import ImageDoc
from connectors.firebase_connector import aupload_image
from connectors.mongodb_connector import acreate_image_doc

async def upload_and_create_image(image_doc: ImageDoc):
    """
    Uploads an image to Firebase and creates an image document in MongoDB
    """
    image_doc = await aupload_image(image_doc)
    print(f"image_doc: {image_doc}") 
    await acreate_image_doc(image_doc)

