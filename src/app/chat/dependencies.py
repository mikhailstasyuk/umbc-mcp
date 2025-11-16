from fastapi import Depends
from openai import OpenAI

from src.app.chat.service import ChatService
from src.app.llm_providers.client import get_chat_openai_client
from src.app.config import Settings, get_settings


def get_chat_service(
        settings: Settings = Depends(get_settings),
        openai_client: OpenAI = Depends(get_chat_openai_client)
) -> ChatService:
    return ChatService(
        openai_client=openai_client
    )
