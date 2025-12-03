from fastapi.testclient import TestClient
from typing import Any
import pytest
from unittest.mock import Mock

from src.app.main import app
from src.app.chat.dependencies import get_chat_service
from src.app.chat.schemas import ChatResponse
from src.app.chat.exceptions import (
    AuthenticationFailedError,
    RateLimitExceededError,
    OpenAIConnectionError,
    EmptyResponseError,
    ModelNotFoundError,
)

payload: dict[str, Any] = {
    "model": "test-model",
    "messages": [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello"},
        {"role": "user", "content": "What is molasses?"},
    ],
}


def test_chat_available(client_with_mock_service: TestClient):
    """Verify the chat endpoint returns 200 OK."""
    response = client_with_mock_service.post("/chat", json=payload)
    assert response.status_code == 200


def test_chat_returns_chat_response(client_with_mock_service: TestClient):
    """Verify the chat endpoint returns a valid ChatResponse."""
    response = client_with_mock_service.post("/chat", json=payload)
    chat_response = ChatResponse(**response.json())
    assert chat_response.message == "Hello Kitty"


@pytest.fixture
def mock_error_service():
    """Fixture that returns a mock service for error testing."""
    return Mock()


@pytest.fixture
def client_with_error_service(mock_error_service: Mock):
    """Test client with a mock service that can raise errors."""
    app.dependency_overrides[get_chat_service] = lambda: mock_error_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_chat_returns_401_on_auth_error(
    client_with_error_service: TestClient,
    mock_error_service: Mock,
):
    """Verify the router returns 401 when authentication fails."""
    mock_error_service.generate_response.side_effect = AuthenticationFailedError(
        message="OpenAI authentication failed: Invalid API key"
    )

    response = client_with_error_service.post("/chat", json=payload)

    assert response.status_code == 401
    assert "authentication" in response.json()["detail"].lower()


def test_chat_returns_429_on_rate_limit(
    client_with_error_service: TestClient,
    mock_error_service: Mock,
):
    """Verify the router returns 429 when rate limit is exceeded."""
    mock_error_service.generate_response.side_effect = RateLimitExceededError(
        message="OpenAI rate limit exceeded"
    )

    response = client_with_error_service.post("/chat", json=payload)

    assert response.status_code == 429
    assert "rate limit" in response.json()["detail"].lower()


def test_chat_returns_502_on_connection_error(
    client_with_error_service: TestClient,
    mock_error_service: Mock,
):
    """Verify the router returns 502 when connection to OpenAI fails."""
    mock_error_service.generate_response.side_effect = OpenAIConnectionError(
        message="Failed to connect to OpenAI API"
    )

    response = client_with_error_service.post("/chat", json=payload)

    assert response.status_code == 502
    assert "connect" in response.json()["detail"].lower()


def test_chat_returns_500_on_empty_response(
    client_with_error_service: TestClient,
    mock_error_service: Mock,
):
    """Verify the router returns 500 when OpenAI returns empty choices."""
    mock_error_service.generate_response.side_effect = EmptyResponseError(
        message="OpenAI returned an empty response"
    )

    response = client_with_error_service.post("/chat", json=payload)

    assert response.status_code == 500
    assert "empty" in response.json()["detail"].lower()


def test_chat_returns_503_on_missing_api_key(
    client_with_error_service: TestClient,
    mock_error_service: Mock,
):
    """Verify the router returns 503 when API key is not configured."""
    mock_error_service.generate_response.side_effect = ValueError(
        "OPENAI_API_KEY is not set"
    )

    response = client_with_error_service.post("/chat", json=payload)

    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_chat_returns_404_on_model_not_found(
    client_with_error_service: TestClient,
    mock_error_service: Mock,
):
    """Verify the router returns 404 when the model does not exist."""
    mock_error_service.generate_response.side_effect = ModelNotFoundError(
        message="Model not found: invalid-model"
    )

    response = client_with_error_service.post("/chat", json=payload)

    assert response.status_code == 404
    assert "model" in response.json()["detail"].lower()


def test_chat_rejects_empty_messages(client_with_mock_service: TestClient):
    """Verify the chat endpoint returns 422 when messages array is empty."""
    empty_messages_payload: dict[str, Any] = {
        "model": "test-model",
        "messages": [],
    }

    response = client_with_mock_service.post("/chat", json=empty_messages_payload)

    assert response.status_code == 422


def test_chat_rejects_oversized_messages(client_with_mock_service: TestClient):
    """Verify the chat endpoint returns 422 when message content exceeds max length."""
    max_content_length = 10000
    oversized_content = "x" * (max_content_length + 1)
    oversized_payload: dict[str, Any] = {
        "model": "test-model",
        "messages": [{"role": "user", "content": oversized_content}],
    }

    response = client_with_mock_service.post("/chat", json=oversized_payload)

    assert response.status_code == 422
