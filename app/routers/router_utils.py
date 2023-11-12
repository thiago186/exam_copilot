"""This file contains utils for the API routes, such as jwt token validation."""

from fastapi import HTTPException, status, Request

from services.auth import verify_jwt_token


def validate_token(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    if token.startswith("Bearer "):
        token = token[7:]

    return verify_jwt_token(token)
