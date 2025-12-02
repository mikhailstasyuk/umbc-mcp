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
    ChatCompletionSystemMessageParam,
)

from src.app.chat.exceptions import (
    AuthenticationFailedError,
    RateLimitExceededError,
    OpenAIConnectionError,
    EmptyResponseError,
    ModelNotFoundError,
)
from src.app.chat.schemas import ChatResponse, CreateChatRequest
from src.app.chat.prompts import get_system_prompt


class ChatService:
    def __init__(
        self,
        *,
        openai_client: OpenAI,
        project_name: str,
        project_description: str,
        base_system_prompt: str,
        chat_history_limit: int,
        max_iterations: int,
        retrieval_top_k: int,
    ):
        self.chat_client = openai_client
        self.project_name = project_name
        self.project_description = project_description
        self.base_system_prompt = base_system_prompt
        self.chat_history_limit = chat_history_limit
        self.max_iterations = max_iterations
        self.retrieval_top_k = retrieval_top_k

    def _create_chat_messages(
        self,
        system_prompt: str,
        chat_history: list[ChatCompletionMessageParam],
        user_message: str,
    ) -> list[ChatCompletionMessageParam]:
        """Create the complete list of chat messages."""
        return [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            *chat_history,
            ChatCompletionUserMessageParam(role="user", content=user_message),
        ]

    def generate_response(self, chat_input: CreateChatRequest) -> ChatResponse:
        """Generate response based on chat input"""
        system_prompt: str = get_system_prompt(
            project_name=self.project_name,
            project_description=self.project_description,
            base_prompt=self.base_system_prompt,
            max_attempts=self.max_iterations,
        )

        # Prepare chat history
        chat_history: list[ChatCompletionMessageParam] = [
            (
                ChatCompletionUserMessageParam(role="user", content=msg.content)
                if msg.role == "user"
                else ChatCompletionAssistantMessageParam(
                    role="assistant", content=msg.content
                )
            )
            for msg in (chat_input.messages or [])[-self.chat_history_limit : -1]
        ]

        messages = self._create_chat_messages(
            system_prompt, chat_history, chat_input.messages[-1].content
        )

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
