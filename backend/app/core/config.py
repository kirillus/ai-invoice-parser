from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=str(Path(__file__).resolve().parents[2] / ".env"),
    env_file_encoding="utf-8",
    extra="ignore",
  )

  APP_NAME: str = 'AI Invoice Parser'
  APP_VERSION: str = "0.0.1"
  DEBUG: bool = True
  API_V1_PREFIX: str = "/api/v1"
  CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
  MAX_FILE_SIZE_MB: int = 10
  ALLOWED_FILE_EXTENSIONS: list[str] = ["pdf", "jpg", "jpeg", "png", "tiff"]
  UPLOAD_DIR: str = "uploads"
  ANTHROPIC_API_KEY: str = ""
  ANTHROPIC_MODEL: str = "claude-haiku-4-5-20251001"


@lru_cache()
def get_settings() -> Settings:
  return Settings()
