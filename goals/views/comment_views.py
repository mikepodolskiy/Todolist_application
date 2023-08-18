from typing import List

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import CommentFilter
from goals.models import Comment
from goals.serializers.comment_serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = CommentFilter
    ordering = ["-created"]

    def get_queryset(self) -> List[Comment]:
        """
        make queryset to provide comments list visibility only to user
        """
        return Comment.objects.select_related("user").filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> List[Comment]:
        """
        make queryset to provide comment visibility only to user
        """
        return Comment.objects.select_related("user").filter(
            user=self.request.user
        )
