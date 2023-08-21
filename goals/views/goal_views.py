from typing import List

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.serializers.goal_serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["category", "priority", "due_date"]
    ordering = ["category", "priority", "due_date"]
    search_fields = ["title", "description"]

    def get_queryset(self) -> QuerySet:
        """
        make queryset to provide goals list visibility only to user, hides archived and deleted goals
        """
        return Goal.objects.filter(category__board__participants__user=self.request.user,
                                   category__is_deleted=False).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """
        make queryset to hides archived goals
        """
        return Goal.objects.exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal) -> None:
        """
        change field status to archived
        """
        instance.status = Goal.Status.archived
        instance.save()
