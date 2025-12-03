from openai import OpenAI
import pytest

from src.app.config import Settings
from src.app.llm_providers.client import (
    OpenAIConfig,
    create_openai_client,
    get_openai_config,
    get_chat_openai_client,
)


def test_create_openai_client_returns_openai_instance():
    config = OpenAIConfig(api_key="test-api-key")
    client = create_openai_client(config)
    assert isinstance(client, OpenAI)


def test_get_openai_config_uses_settings_api_key():
    settings = Settings(OPENAI_API_KEY="my-secret-key")
    config = get_openai_config(settings)
    assert config.api_key == "my-secret-key"


def test_get_openai_config_raises_without_api_key():
    settings = Settings(OPENAI_API_KEY=None)
    with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
        get_openai_config(settings)


def test_get_chat_openai_client_returns_openai_instance():
    """Verify get_chat_openai_client wires up config and returns OpenAI client."""
    settings = Settings(OPENAI_API_KEY="test-api-key")
    client = get_chat_openai_client(settings=settings)
    assert isinstance(client, OpenAI)
