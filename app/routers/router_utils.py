"""This file contains utils for the API routes, such as jwt token validation."""

from fastapi import HTTPException, status, Request, Depends

from services.auth import verify_jwt_token, decrypt_jwt


def get_cookie_from_request(request: Request):
    """Returns the jwt token from the request cookies"""

    token = request.cookies.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    if token.startswith("Bearer "):
        token = token[7:]
        return token

def validate_token(request: Request):
    """ Validates the jwt token passed on the request"""
    
    token = get_cookie_from_request(request)
    
    return verify_jwt_token(token)

def get_user_id_from_jwt(request: Request):
    """Returns the user_id from the a given jwt token passed on the request"""
    
    token = get_cookie_from_request(request)
    decoded_token = decrypt_jwt(token)

    return decoded_token["user_id"]
