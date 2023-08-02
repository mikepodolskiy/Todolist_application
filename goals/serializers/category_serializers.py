from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.serializers import UserSerializer
from goals.models import GoalCategory, BoardParticipant


class BaseGoalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def validate_board(self, board):
        if board.is_deleted:
            raise ValidationError("The board was deleted")
        if not BoardParticipant.objects.filter(board_id=board.id, user=self.context['request'].user,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
                                               ).exists():
            raise PermissionDenied

        return board

class GoalCategoryCreateSerializer(BaseGoalCategorySerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # default = serializers.CurrentUserDefault()


class GoalCategorySerializer(BaseGoalCategorySerializer):
    user = UserSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")
