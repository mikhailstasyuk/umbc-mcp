from src.app.chat.schemas import ChatResponse
from openai.types.chat import ChatCompletionMessageParam
from openai import OpenAI


class ChatService():
    def __init__(self, openai_client: OpenAI):
        self.openai_client = openai_client

    def generate_response(
            self, 
            model: str,
            messages: list[ChatCompletionMessageParam]
    ) -> ChatResponse:
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
        )
        message = response.choices[0].message
        return ChatResponse(message=message.content)
