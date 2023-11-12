"""This module contains functions for encrypting and verifying fields."""

import time

import bcrypt
import jwt
from fastapi import HTTPException, status

from config import settings


def encrypt_field(field: str):
    """Encrypts a field using bcrypt."""
    hashed_field = bcrypt.hashpw(field.encode("utf-8"), bcrypt.gensalt())
    return hashed_field.decode("utf-8")


def verify_field(field: str, hashed_field: str):
    """Verifies a field using bcrypt."""
    return bcrypt.checkpw(field.encode("utf-8"), hashed_field.encode("utf-8"))


def generate_jwt_token(user_id: str, exp:int=settings.ACCESS_TOKEN_EXPIRE_SECONDS):
    """Generates a JWT token."""
    payload = {
        "user_id": user_id,
        "exp": time.time() + exp,
    }
    token = jwt.encode(
        payload, settings.JWT_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return token


def verify_jwt_token(token: str):
    """Verifies a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_AUTH_SECRET, settings.JWT_ALGORITHM)
        return payload["user_id"]

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
