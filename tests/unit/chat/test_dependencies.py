from unittest.mock import Mock

from openai import OpenAI

from src.app.chat.dependencies import get_chat_service
from src.app.chat.service import ChatService
from src.app.config import Settings


def test_get_chat_service_creates_service_with_settings():
    """Verify get_chat_service wires up ChatService with correct settings."""
    mock_openai_client = Mock(spec=OpenAI)
    settings = Settings(
        PROJECT_NAME="Test Project",
        PROJECT_DESCRIPTION="Test Description",
        BASE_SYSTEM_PROMPT="Test Prompt",
        CHAT_HISTORY_LIMIT=10,
        MAX_CHAT_ITERATIONS=3,
        RETRIEVAL_TOP_K=5,
    )

    service = get_chat_service(
        settings=settings,
        openai_client=mock_openai_client,
    )

    assert isinstance(service, ChatService)
    assert service.project_name == "Test Project"
    assert service.project_description == "Test Description"
    assert service.base_system_prompt == "Test Prompt"
    assert service.chat_history_limit == 10
    assert service.max_iterations == 3
    assert service.retrieval_top_k == 5
    assert service.chat_client is mock_openai_client
