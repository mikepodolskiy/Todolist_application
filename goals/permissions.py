from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj, role=BoardParticipant.Role.owner).exists()


class GoalCategoryPermission(permissions.IsAuthenticated):
    def has_oblect_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj.board).exclude(
            role=BoardParticipant.Role.reader).exists()


class GoalPermission(permissions.IsAuthenticated):
    def has_oblect_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exclude(
            role=BoardParticipant.Role.reader).exists()


class CommentPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
