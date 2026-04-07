from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
  APP_NAME: str = 'AI Invoice Parser'
  APP_VERSION: str = "0.0.1"
  DEBUG: bool = True
  API_V1_PREFIX: str = "/api/v1"
  CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
  MAX_FILE_SIZE_MB: int = 10
  ALLOWED_FILE_EXTENSIONS: list[str] = ["pdf", "jpg", "jpeg", "png", "tiff"]
  UPLOAD_DIR: str = "uploads"

  class config:
    env_file: str = ".env"


@lru_cache()
def get_settings() -> Settings:
  return Settings()
