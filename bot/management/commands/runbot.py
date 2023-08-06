from django.core.management import BaseCommand

from bot.tg.client import TgClient
from bot.tg.dc import Message


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()


    def handle(self, *args, **kwargs):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            if not res:
                continue
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        self.tg_client.send_message(chat_id=msg.chat.id, text=msg.text)


