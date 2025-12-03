from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    # Application Configuration
    PROJECT_NAME: str = "The current project"
    PROJECT_DESCRIPTION: str = "The current project decription"

    # Provide Configuration
    OPENAI_API_KEY: str | None = None

    # Chat Settings
    BASE_SYSTEM_PROMPT: str = "You are an AI assistant specialized in retrieving and synthesizing information to provide relevant answers to queries."
    CHAT_HISTORY_LIMIT: int = 20
    MAX_CHAT_ITERATIONS: int = 5
    RETRIEVAL_TOP_K: int = 10
    MAX_MESSAGE_LENGTH: int = 10000


@lru_cache
def get_settings():
    return Settings()
