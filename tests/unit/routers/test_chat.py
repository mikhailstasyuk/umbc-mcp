from fastapi.testclient import TestClient
from typing import Any

from src.app.chat.schemas import ChatResponse

payload: dict[str, Any] = {
    "model": "test-model", 
    "messages": [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello"},
        {"role": "user", "content": "What is molasses?"},
    ]
}


def test_chat_available(client_with_mock_service: TestClient):
    response = client_with_mock_service.post("/chat", json=payload)
    assert response.status_code == 200


def test_chat_returns_chat_response(client_with_mock_service: TestClient):
    response = client_with_mock_service.post("/chat", json=payload)
    chat_response = ChatResponse(**response.json())
    assert chat_response.message == "Hello Kitty"
