from dataclasses import dataclass
from fastapi import Depends
from openai import OpenAI
from src.app.config import Settings, get_settings


@dataclass
class OpenAIConfig:
    api_key: str


def create_openai_client(config: OpenAIConfig) -> OpenAI:
    return OpenAI(api_key=config.api_key)


def get_openai_config(settings: Settings):
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")
    return OpenAIConfig(api_key=settings.OPENAI_API_KEY)


def get_chat_openai_client(settings: Settings = Depends(get_settings)) -> OpenAI:
    config = get_openai_config(settings=settings)
    return create_openai_client(config)
