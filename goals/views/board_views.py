from typing import List

from django.db import transaction
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Board, Goal
from goals.permissions import BoardPermission
from goals.serializers.board_serializers import BoardCreateSerializer, BoardSerializer, BoardListSerializer


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    ordering = ["title"]
    ordering_fields = ["title"]

    def get_queryset(self) -> List[Board]:
        """
        make queryset to provide board list visibility only to user
        """

        return Board.objects.filter(
            participants__user=self.request.user,
            is_deleted=False
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer

    def get_queryset(self) -> List[Board]:
        """
        make queryset to provide board visibility only to user
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> Board:
        """
        Change field is_deleted status to True (the same as delete, but board will stay in db)
        archiving (status=archived) goals of this board
        """
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance
