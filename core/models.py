from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    password = models.CharField()
    password_repeat = models.CharField()


    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.password == self.password_repeat:
            self.set_password(raw_password=self.password)
            super().save(*args, **kwargs)
        raise serializers.ValidationError("Password don't match")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
