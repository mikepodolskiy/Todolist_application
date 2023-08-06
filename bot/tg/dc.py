from dataclasses import dataclass
from pydantic import BaseModel
from typing import List


class Chat(BaseModel):
    id: int
    username: str | None = None


class Update(BaseModel):
    ok: bool
    result: List


class Message(BaseModel):
    message_id: int
    chat: Chat
    text: str


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: List[UpdateObj]
    # class Meta:
    #     unknown = EXCLUDE


class SendMessageResponse:
    ok: bool
    result: Message

    # class Meta:
    #     unknown = EXCLUDE
