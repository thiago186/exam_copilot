from dotenv import load_dotenv
from pydantic.env_settings import BaseSettings
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
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
