from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.serializers import UserSerializer
from goals.models import Comment, BoardParticipant, Goal


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, goal):
        if goal.status == Goal.Status.archived:
            raise ValidationError("The goal was deleted")
        if not BoardParticipant.objects.filter(board_id=goal.category.board_id,
                                               user=self.context['request'].user,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
                                               ).exists():
            raise PermissionDenied
        return goal


    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')
