import os
from typing import Any

from dotenv import load_dotenv
from pydantic.env_settings import BaseSettings
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    LOG_LEVEL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    SQL_ECHO: bool = True
    USERS_RESET_PASSWORD_ENCRYPTED: str
    JWT_AUTH_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: str
    MONGO_DB: str
    FIREBASE_CREDENTIALS_FILENAME: str
    FIREBASE_BUCKET_URL: str
    LOCAL_MEDIA_PATH: str

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not os.path.exists(self.LOCAL_MEDIA_PATH):
            os.makedirs(self.LOCAL_MEDIA_PATH)

    @property
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=f"/{self.POSTGRES_DB}",
        )


settings = Settings()
