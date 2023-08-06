import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist_diplom import settings
from todolist_diplom.settings import BOT_TOKEN


class TgClient:
    def __init__(self, token=None):
        self.__token = token if token else settings.BOT_TOKEN

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.__token}/{method}"

    def _get_response(self, method, payload):
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



# client = TgClient()
# resp = client.get_updates()
# print(resp)
# mess = client.send_message(447221072, "another test2")
# print(mess)
