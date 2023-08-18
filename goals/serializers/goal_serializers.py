from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.serializers import UserSerializer
from goals.models import Goal, BoardParticipant, GoalCategory


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        """
        validates category and user's role

        """

        if category.is_deleted:
            raise ValidationError("The category was deleted")
        if not BoardParticipant.objects.filter(board_id=category.board_id, user=self.context['request'].user,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
                                               ).exists():
            raise PermissionDenied("Permission denied")

        return category


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')
