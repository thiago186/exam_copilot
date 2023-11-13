"""This code contains the FastAPI main application."""

from typing import Annotated

from fastapi import Depends, FastAPI

from routers import login
from routers import images
from routers import questions
from schemas.users import User
from schemas.items import ImageDoc


app = FastAPI()

app.include_router(login.router)
app.include_router(images.router)
app.include_router(questions.router)
