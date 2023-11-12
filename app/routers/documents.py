"""
This file handles the documents routes, including receiving images to save on database and storage bucket.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from config import settings
from routers.router_utils import validate_token
from schemas.items import ImageDoc
from services.items_service import upload_and_create_image

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(validate_token)],
)


@router.post("/receive_file", status_code=200)
async def create_image(file: UploadFile):
# async def create_image(image_data: ImageDoc):
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
