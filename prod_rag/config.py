from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    groq_api_key: SecretStr | None = None
    chroma_db_path: str = str(Path(__file__).resolve().parents[1] / "db" / "chroma")
    langsmith_api_key: SecretStr | None = None


settings = Settings()
