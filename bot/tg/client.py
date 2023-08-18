from typing import Optional

import requests
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist_diplom.settings import BOT_TOKEN


class TgClient:
    def __init__(self, token: str | None = None):
        self.__token = token if token else BOT_TOKEN

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.__token}/{method}"

    def _get_response(self, method: str, payload: dict) -> Optional[GetUpdatesResponse, SendMessageResponse]:
        response = requests.get(self.get_url(method), params=payload)
        return response.json()

    def get_updates(self, offset: int = 0, timeout: int = 5) -> GetUpdatesResponse:
        method = "getUpdates"
        payload = {
            "offset": offset,
            "timeout": timeout,
        }
        response = self._get_response(method, payload)
        return GetUpdatesResponse(**response)

    def send_message(self, chat_id: int, text: str, timeout: int = 5) -> SendMessageResponse:
        method = "sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "timeout": timeout,

        }
        return self._get_response(method, payload)
