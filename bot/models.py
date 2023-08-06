from django.db import models
from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    verification_code = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.__class__.__name__}({self.tg_chat_id})'


    class Meta:
        verbose_name = "Телеграм пользователь"
        verbose_name_plural = "Телеграм пользователи"
