"""This module contains the login related routes."""

import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from fastapi.security import OAuth2PasswordBearer

from config import settings
import connectors.users_connector as users_connector
from routers.router_utils import validate_token
from services.auth import verify_jwt_token
from schemas.users import User, UserBase
from utils.exceptions import AuthenticationError

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("")
async def login(user_base: UserBase, response: Response):
    """Logs in the user."""
    try:
        auth = await users_connector.authenticate_user(user_base.email, user_base.password)
        response.set_cookie(
            key="token",
            value=f"Bearer {auth['jwt']}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            secure=True,
            samesite="None"
        )
        return {"detail": "User authenticated with success."}

    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")


@router.post("/create-user")
async def create_user(user_base: UserBase):
    """Creates the user in the database."""
    user = User(**user_base.dict())
    user.set_password(user_base.password)
    logging.debug(f"Password set using hashing algorithm.")
    try:
        await users_connector.create_user(user)
        return {"detail": "User created successfully."}

    except Exception as e:
        if str(e) == "User already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists.")

@router.post("/reset-user-pwd", include_in_schema=False) 
async def reset_user_password(token: str, user_email: str, new_password: str):
    """
    Resets user's password if given the correct token.
    For the purpose of testing, the token is hardcoded in .env.
    TODO: 
    Deal gracefully with the case of how to correctly reset passwords
    """
    if token == settings.USERS_RESET_PASSWORD_ENCRYPTED:
        print(f"trying to change id: {user_email}")
        await users_connector.change_user_password(user_email, new_password)
        return {"detail": "Password reset successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

@router.get("/test-dependency")
async def test(user_id: Annotated[str, Depends(validate_token)]):
    return {"user_id": user_id}