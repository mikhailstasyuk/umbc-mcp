from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
)
from openai.types.chat.chat_completion import Choice
from pytest_mock import MockerFixture

from src.app.chat.service import ChatService
from src.app.chat.schemas import (
    ChatMessage, 
    CreateChatRequest, 
    ChatResponse
)


def test_chat_service_calls_openai(
        mock_service: ChatService,
        mock_openai_client: OpenAI,
        mocker: MockerFixture,
)-> None:
    mock_completion = ChatCompletion(
        id="test-id",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content="This is a model response",
                    role="assistant",
                ),
            )
        ],
        created=1234567890,
        model="test-model",
        object="chat.completion",
    )
    mock_create_completion = mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mock_completion
    )
    response = mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )
    mock_create_completion.assert_called_once()


def test_chat_service_passes_messages_and_model(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    mock_create = mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content="ok"))])
    )
    mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )
    mock_create.assert_called_once_with(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )

def test_chat_service_returns_chat_response_object(
        mock_service: ChatService,
        mock_openai_client: OpenAI,
        mocker: MockerFixture,
)-> None:
    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content="ok"))]
        )
    )
    response = mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )
    assert isinstance(response, ChatResponse)
    assert isinstance(response.message, str)
    assert response.message == "ok"
    

def test_chat_service_handles_none_message(
        mock_service: ChatService,
        mock_openai_client: OpenAI,
        mocker: MockerFixture,
)-> None:
    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content=None))]
        )
    )

    response = mock_service.generate_response(
        messages=[{"role": "user", "content": "Hi"}],
        model="test-model",
    )

    assert isinstance(response, ChatResponse)
    assert response.message is None


def test_create_chat_request_valid():
    request = CreateChatRequest(
        model="test-model",
        messages=[
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Hello"),
        ]
    )
    assert isinstance(request, CreateChatRequest)
    assert request.model == "test-model"
    assert request.messages is not None
    assert len(request.messages) == 2
    assert request.messages[0].role == "user"


def test_chat_message_valid():
    message = ChatMessage(
        role="user",
        content="Hi",
    )
    assert isinstance(message, ChatMessage)
    assert message.role == "user"
    assert message.content == "Hi"
