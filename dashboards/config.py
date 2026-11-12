from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DB_DRIVER: str = "postgresql+psycopg"
    DB_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=self.DB_DRIVER,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB
        )


settings = Settings()