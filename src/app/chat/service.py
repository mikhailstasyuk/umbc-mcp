from openai import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    NotFoundError,
    OpenAI,
)
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)

from src.app.chat.exceptions import (
    AuthenticationFailedError,
    RateLimitExceededError,
    OpenAIConnectionError,
    EmptyResponseError,
    ModelNotFoundError,
)
from src.app.chat.schemas import ChatResponse, CreateChatRequest


class ChatService:
    def __init__(self, openai_client: OpenAI):
        self.chat_client = openai_client

    def generate_response(self, chat_input: CreateChatRequest) -> ChatResponse:
        messages: list[ChatCompletionMessageParam] = [
            (
                ChatCompletionUserMessageParam(role="user", content=msg.content)
                if msg.role == "user"
                else ChatCompletionAssistantMessageParam(
                    role="assistant", content=msg.content
                )
            )
            for msg in (chat_input.messages or [])
        ]

        try:
            response = self.chat_client.chat.completions.create(
                model=chat_input.model,
                messages=messages,
            )
        except AuthenticationError as e:
            raise AuthenticationFailedError(
                message=f"OpenAI authentication failed: {e.message}"
            )
        except RateLimitError as e:
            raise RateLimitExceededError(
                message=f"OpenAI rate limit exceeded: {e.message}"
            )
        except APIConnectionError:
            raise OpenAIConnectionError(message="Failed to connect to OpenAI API")
        except NotFoundError as e:
            raise ModelNotFoundError(message=f"Model not found: {e.message}")

        if not response.choices:
            raise EmptyResponseError(message="OpenAI returned an empty response")

        message = response.choices[0].message
        return ChatResponse(message=message.content)
