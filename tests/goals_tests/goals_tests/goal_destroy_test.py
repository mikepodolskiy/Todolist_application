import pytest

from goals.models import Goal


class TestGoalDestroy:
    @pytest.mark.django_db
    def test_goal_destroy(self, client_and_goal):
        client, goal = client_and_goal

        response = client.delete(
            f"/goals/goal/{goal.pk}"
        )
        assert response.status_code == 204, f"{response.status_code} instead of 204"

        goal.refresh_from_db()
        assert goal.status == Goal.Status.archived, "Goal was not marked as archived"
