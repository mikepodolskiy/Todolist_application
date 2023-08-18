import datetime

import pytest
from goals.models import Goal


class TestGoalCreate:
    @pytest.mark.django_db
    def test_goal_create(self, client_and_category):
        client, category = client_and_category

        data = {
            "title": "new_title",
            "description": "description",
            "due_date": "2022-02-03",
            "priority": Goal.Status.to_do,
            "status": Goal.Priority.low,
            "category": category.pk,
        }
        response = client.post(
            "/goals/goal/create",
            data=data,
            content_type="application/json"
        )
        assert response.status_code == 201, f"{response.status_code} instead of 201"

        data["category"] = category
        data["due_date"] = datetime.date.fromisoformat(data["due_date"])
        data["user"] = category.user

        created_goal = Goal.objects.last()

        assert created_goal.title == data["title"], "Incorrect title"
        assert created_goal.description == data["description"], "Incorrect description"
        assert created_goal.due_date == data["due_date"], "Incorrect due_date"
        assert created_goal.priority == data["priority"], "Incorrect due_date"
        assert created_goal.status == data["status"], "Incorrect due_date"
        assert created_goal.category == data["category"], "Incorrect due_date"
