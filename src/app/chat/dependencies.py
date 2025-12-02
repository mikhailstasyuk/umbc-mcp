from fastapi import Depends
from openai import OpenAI

from src.app.chat.service import ChatService
from src.app.llm_providers.client import get_chat_openai_client
from src.app.config import Settings, get_settings


def get_chat_service(
    settings: Settings = Depends(get_settings),
    openai_client: OpenAI = Depends(get_chat_openai_client),
) -> ChatService:
    return ChatService(
        openai_client=openai_client,
        project_name=settings.PROJECT_NAME,
        project_description=settings.PROJECT_DESCRIPTION,
        base_system_prompt=settings.BASE_SYSTEM_PROMPT,
        chat_history_limit=settings.CHAT_HISTORY_LIMIT,
        max_iterations=settings.MAX_CHAT_ITERATIONS,
        retrieval_top_k=settings.RETRIEVAL_TOP_K,
    )
