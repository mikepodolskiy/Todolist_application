from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True,
                                     validators=[validate_password])
    password_repeat = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, attrs: dict) -> dict:
        """
        compare password and repeat password fields, rase error if not match
        """
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError("Passwords should match")
        return attrs

    def create(self, validated_data: dict) -> Any:
        """
        create user in db with hashed password
        """
        validated_data["password"] = make_password(validated_data["password"])
        validated_data.pop("password_repeat")

        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True,
                                     validators=[validate_password])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True,
                                         validators=[validate_password])

    def validate_old_password(self, old_password: str) -> str:

        request = self.context["request"]

        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated

        if not request.user.check_password(old_password):
            raise exceptions.ValidationError("Wrong password")

        return old_password
