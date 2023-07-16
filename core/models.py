from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers


class User(AbstractUser):


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
