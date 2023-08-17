from rest_framework import response, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from core.models import User
from bot.management.commands.runbot import Command
from bot.serializers.bot_serializer import BotVerificationSerializer


from rest_framework.views import APIView, Response
from rest_framework import permissions, status

from .models import TgUser

from .tg.client import TgClient
from todolist_diplom.settings import BOT_TOKEN


class BotVerificationView(UpdateAPIView):
    serializer_class = BotVerificationSerializer
    permission_classes = [IsAuthenticated]
    success_answer = "Successful verification"

    def get_object(self):
        return self.request.user




    def perform_update(self, request):
        verification_code = self.request.data["verification_code"]
        tg_user = TgUser.objects.get(verification_code=verification_code)
        tg_user.user_id = self.get_object()
        tg_user.save()

        tg_client = TgClient()
        tg_client.send_message(chat_id=tg_user.tg_chat_id,
                               text=self.success_answer
                               )
        return response.Response(self.success_answer,
                                 status=status.HTTP_200_OK
                                 )


