import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = ""
    PORT: int = 5000
    NODE_ENV: str = "development"
    CLIENT_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
