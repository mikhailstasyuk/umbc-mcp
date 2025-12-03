from typing import Annotated, Literal
from pydantic import BaseModel, Field

from src.app.config import get_settings

_settings = get_settings()


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: Annotated[str, Field(max_length=_settings.MAX_MESSAGE_LENGTH)]


class CreateChatRequest(BaseModel):
    model: str
    messages: Annotated[list[ChatMessage], Field(min_length=1)]


class ChatResponse(BaseModel):
    message: str | None
