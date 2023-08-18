from rest_framework import permissions

from goals.models import BoardParticipant, Board, GoalCategory, Goal


class BoardPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Board) -> bool:
        """
        divides permissions for get method and other methods
        """
        if request.method == "GET":
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj, role=BoardParticipant.Role.owner).exists()


class GoalCategoryPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory) -> bool:
        """
        divides permissions for safe methods (allowed for anyone) and other methods (not allowed for reader)
        """
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj.board).exclude(
            role=BoardParticipant.Role.reader).exists()


class GoalPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal) -> bool:
        """
        divides permissions for safe methods (allowed for anyone) and other methods (not allowed for reader)
        """

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exclude(
            role=BoardParticipant.Role.reader).exists()


class CommentPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        """
        provides permission to comment goal only for author, and read for anyone authenticated
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
