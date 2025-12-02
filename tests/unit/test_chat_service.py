import httpx
import pytest
from openai import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    NotFoundError,
    OpenAI,
)
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
)
from openai.types.chat.chat_completion import Choice
from pytest_mock import MockerFixture

from src.app.chat.exceptions import (
    AuthenticationFailedError,
    RateLimitExceededError,
    OpenAIConnectionError,
    EmptyResponseError,
    ModelNotFoundError,
)
from src.app.chat.service import ChatService
from src.app.chat.schemas import ChatMessage, CreateChatRequest, ChatResponse


def test_chat_service_calls_openai(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
) -> None:
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
        mock_openai_client.chat.completions, "create", return_value=mock_completion
    )
    chat_input: CreateChatRequest = CreateChatRequest(
        model="test-model",
        messages=[
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Ok"),
        ],
    )
    mock_service.generate_response(chat_input)
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
            choices=[mocker.Mock(message=mocker.Mock(content="ok"))]
        ),
    )
    chat_input: CreateChatRequest = CreateChatRequest(
        model="test-model",
        messages=[
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Ok"),
        ],
    )
    mock_service.generate_response(chat_input)
    mock_create.assert_called_once_with(
        messages=[
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Ok"},
        ],
        model="test-model",
    )


def test_chat_service_returns_chat_response_object(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content="ok"))]
        ),
    )
    chat_input: CreateChatRequest = CreateChatRequest(
        model="test-model",
        messages=[
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Ok"),
        ],
    )
    response = mock_service.generate_response(chat_input)
    assert isinstance(response, ChatResponse)
    assert isinstance(response.message, str)
    assert response.message == "ok"


def test_chat_service_handles_none_message(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content=None))]
        ),
    )
    chat_input: CreateChatRequest = CreateChatRequest(
        model="test-model",
        messages=[
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Hello"),
        ],
    )
    response = mock_service.generate_response(chat_input)

    assert isinstance(response, ChatResponse)
    assert response.message is None


def test_create_chat_request_valid():
    request = CreateChatRequest(
        model="test-model",
        messages=[
            ChatMessage(role="user", content="Hi"),
            ChatMessage(role="assistant", content="Hello"),
        ],
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


def test_chat_service_handles_openai_auth_error(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    """Service should raise AuthenticationFailedError when OpenAI auth fails."""
    mock_response = httpx.Response(
        status_code=401,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )
    auth_error = AuthenticationError(
        "Incorrect API key provided",
        response=mock_response,
        body={
            "error": {
                "message": "Incorrect API key provided",
                "type": "invalid_request_error",
            }
        },
    )

    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        side_effect=auth_error,
    )

    chat_input = CreateChatRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
    )

    with pytest.raises(AuthenticationFailedError) as exc_info:
        mock_service.generate_response(chat_input)

    assert exc_info.value.status_code == 401
    assert "authentication" in exc_info.value.message.lower()


def test_chat_service_handles_openai_rate_limit_error(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    """Service should raise RateLimitExceededError when OpenAI rate limit is hit."""
    mock_response = httpx.Response(
        status_code=429,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )
    rate_limit_error = RateLimitError(
        "Rate limit exceeded",
        response=mock_response,
        body={"error": {"message": "Rate limit exceeded", "type": "rate_limit_error"}},
    )

    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        side_effect=rate_limit_error,
    )

    chat_input = CreateChatRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
    )

    with pytest.raises(RateLimitExceededError) as exc_info:
        mock_service.generate_response(chat_input)

    assert exc_info.value.status_code == 429
    assert "rate limit" in exc_info.value.message.lower()


def test_chat_service_handles_openai_api_connection_error(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    """Service should raise OpenAIConnectionError when connection fails."""
    connection_error = APIConnectionError(
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )

    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        side_effect=connection_error,
    )

    chat_input = CreateChatRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
    )

    with pytest.raises(OpenAIConnectionError) as exc_info:
        mock_service.generate_response(chat_input)

    assert exc_info.value.status_code == 502
    assert "connect" in exc_info.value.message.lower()


def test_chat_service_handles_empty_choices(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    """Service should raise EmptyResponseError when choices array is empty."""
    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        return_value=mocker.Mock(choices=[]),  # Empty choices array
    )

    chat_input = CreateChatRequest(
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")],
    )

    with pytest.raises(EmptyResponseError) as exc_info:
        mock_service.generate_response(chat_input)

    assert exc_info.value.status_code == 500
    assert "empty" in exc_info.value.message.lower()


def test_chat_service_handles_model_not_found(
    mock_service: ChatService,
    mock_openai_client: OpenAI,
    mocker: MockerFixture,
):
    """Service should raise ModelNotFoundError when model does not exist."""
    mock_response = httpx.Response(
        status_code=404,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )
    not_found_error = NotFoundError(
        "The model `invalid-model` does not exist",
        response=mock_response,
        body={
            "error": {
                "message": "The model does not exist",
                "type": "invalid_request_error",
                "code": "model_not_found",
            }
        },
    )

    mocker.patch.object(
        mock_openai_client.chat.completions,
        "create",
        side_effect=not_found_error,
    )

    chat_input = CreateChatRequest(
        model="invalid-model",
        messages=[ChatMessage(role="user", content="Hi")],
    )

    with pytest.raises(ModelNotFoundError) as exc_info:
        mock_service.generate_response(chat_input)

    assert exc_info.value.status_code == 404
    assert "model" in exc_info.value.message.lower()
