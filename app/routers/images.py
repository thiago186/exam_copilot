"""
This file handles the images routes, including receiving images to save on database and storage bucket.
"""

from typing import Annotated
import os

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from config import settings
from routers.router_utils import validate_token
from schemas.items import ImageDoc
from services.items_service import aupload_and_create_image


router = APIRouter(
    prefix="/images",
    tags=["images"],
    dependencies=[Depends(validate_token)],
)


@router.post("/receive-file", status_code=200)
async def receive_document(file: UploadFile):
    """
    This function receives a file and save it to the media local folder.
    """
    
    try:
        file_location = f"{settings.LOCAL_MEDIA_PATH}/{file.filename}"
        with open(file_location, "wb") as file_object:
            file_object.write(await file.read())

        return {"detail": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-image" , status_code=200)
async def create_image_doc(image_data: ImageDoc):
    """
    This function receives an image document data, checks on 
    media directory if the image exists, and if it does, uploads
    it to the bucket and creates the document on the database.
    """

    if not any(image_data.name in filename for filename in os.listdir(settings.LOCAL_MEDIA_PATH)):
        raise HTTPException(
            status_code=404, detail="Image not found on media directory")
    
    try:
        image_data = await aupload_and_create_image(image_data)
        return {"detail": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
