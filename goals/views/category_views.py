from typing import List

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory
from goals.permissions import GoalCategoryPermission
from goals.serializers.category_serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_field = ["board"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self) -> List[GoalCategory]:
        """
        make queryset to provide categories list visibility only to user
        """
        return GoalCategory.objects.select_related(
            "user").filter(

            board__participants__user=self.request.user, is_deleted=False,
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]

    def get_queryset(self) -> List[GoalCategory]:
        """
        make queryset to provide category visibility only to user
        """

        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        instance.is_deleted = True
        instance.save()
        return instance
