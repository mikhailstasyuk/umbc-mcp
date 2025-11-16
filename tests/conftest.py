from fastapi.testclient import TestClient
from openai import OpenAI
import pytest
from pytest_mock import MockerFixture

from src.app.main import app
from src.app.chat.dependencies import get_chat_service
from src.app.chat.service import ChatService


@pytest.fixture
def mock_service(mock_openai_client: OpenAI):
    return ChatService(
        openai_client=mock_openai_client
    )


@pytest.fixture
def mock_openai_client(mocker: MockerFixture) -> OpenAI:
    client = mocker.Mock(spec=OpenAI)
    client.chat = mocker.Mock()
    client.chat.completions = mocker.Mock()
    return client


@pytest.fixture
def client_with_mock_service(mock_service: ChatService):
    app.dependency_overrides[get_chat_service] = lambda: mock_service
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()
