from fastapi import Depends
from openai import OpenAI

from src.app.chat.service import ChatService
from src.app.llm_providers.client import get_chat_openai_client


def get_chat_service(
    openai_client: OpenAI = Depends(get_chat_openai_client),
) -> ChatService:
    return ChatService(openai_client=openai_client)
