"""This file contains the connector for the users table."""

import logging
from sqlmodel import SQLModel, Session, create_engine, select

from dotenv import load_dotenv

from config import settings
from services.auth import (
    verify_field,
    encrypt_field,
    generate_jwt_token,
    verify_jwt_token
)
from schemas.users import User
from utils.exceptions import AuthenticationError, UserNotFoundError


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=settings.SQL_ECHO)


def build_tables(password):
    """
    Create all tables that don't exist in the database.
    This function is only available for the admin user.
    """
    if verify_field(password, settings.USERS_RESET_PASSWORD_ENCRYPTED):
        SQLModel.metadata.create_all(engine)
    else:
        print("You don't have permission to do this. Users will not be reseted.")


def reset_tables(password):
    """
    Reset all the tables in the database.
    This function is only available for the admin user.
    """
    if verify_field(password, settings.USERS_RESET_PASSWORD_ENCRYPTED):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    else:
        print("You don't have permission to do this. Users will not be reseted.")


async def get_user_by_email(email: str):
    """
    Get a user by its email.
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        users = session.exec(statement)
        return users.first()


async def get_user_by_id(user_id: str):
    """
    Get a user by its email.
    """
    with Session(engine) as session:
        statement = select(User).where(User.user_id == user_id)
        users = session.exec(statement)
        return users.first()


async def create_user(user: User):
    """
    Create a new user in the database.
    """
    if not await get_user_by_email(user.email):
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    else:
        raise Exception("User already exists.")


async def update_user_active_status(user_id: int, active: bool):
    """
    Update a user's 'active' attribute in the database.
    """
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            user.active = active
            session.commit()
            session.refresh(user)
            return user


async def change_user_password(user_email: str, new_password: str):
    """
    Change user's password
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == user_email)
        user = session.exec(statement).first()
        logging.debug(f"Found user: {user}")
        if user:
            hashed_new_password = encrypt_field(new_password)
            user.hashed_password = hashed_new_password
            session.commit()
            session.refresh(user)
            return user
    
    raise UserNotFoundError("User not found")


async def authenticate_user(user_email: str, password):
    """
    Authenticate a user.
    """
    user = await get_user_by_email(user_email)

    if not user:
        raise AuthenticationError("User not found")
    
    if not verify_field(password, user.hashed_password):
        raise AuthenticationError("Invalid credentials")
    
    jwt = generate_jwt_token(str(user.user_id))

    return {"jwt": jwt}
