"""This code contains the FastAPI main application."""

from typing import Annotated

from fastapi import Depends, FastAPI

from routers import login
from schemas.users import User


app = FastAPI()

app.include_router(login.router)
