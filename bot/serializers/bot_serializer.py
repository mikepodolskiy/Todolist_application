from rest_framework import serializers
from bot.models import TgUser
from core.models import User


class BotVerificationSerializer(serializers.ModelSerializer):

    def validate_verification_code(self, verification_code):
        """
        checks if user with verification code, that was sent is in the db
        """
        if not TgUser.objects.filter(
                verification_code=verification_code
        ).exists():
            raise serializers.ValidationError("Verification code does not match")
        return verification_code

    class Meta:
        model = User
        id = serializers.IntegerField(read_only=True)
        fields = ['verification_code']
