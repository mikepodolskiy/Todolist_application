import pytest
import datetime
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from goals.serializers.goal_serializers import GoalSerializer
from tests.factories import GoalCategoryFactory, GoalFactory
from goals.models import Goal


class TestGoalUpdate:
    @pytest.mark.django_db
    def test_goal_update(self, client_and_goal):
        client, goal = client_and_goal
        new_category = GoalCategoryFactory(user=goal.user)

        data = {
            "title": "new title",
            "description": "new description",
            "due_date": "2022-02-23",
            "priority": Goal.Status.done,
            "status": Goal.Priority.low,
            "category": new_category.pk,
        }
        response = client.put(
            f"/goals/goal/{goal.pk}",
            data=data,
            content_type="application/json"
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"

        data["due_date"] = datetime.date.fromisoformat(data["due_date"])
        data["category"] = new_category
        goal.refresh_from_db()
        assert response.data == GoalSerializer(goal).data, "Incorrect data"
        for field, value in data.items():
            assert getattr(goal, field) == value, f"Неверное значение поля {field}"
        assert response.data["title"] == data["title"], "Title was not changed"
        assert response.data["description"] == data["description"], "Description was not changed"
        assert response.data["priority"] == data["priority"], "Priority was not changed"
        assert response.data["status"] == data["status"], "Status was not changed"


