from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField


class User(AbstractUser):
    verification_code: CharField = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
