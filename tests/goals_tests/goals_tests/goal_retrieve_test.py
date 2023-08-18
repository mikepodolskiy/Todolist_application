import pytest

from goals.serializers.goal_serializers import GoalSerializer


class TestGoalRetrieve:
    @pytest.mark.django_db
    def test_goal_retrieve(self, client_and_goal):
        client, goal = client_and_goal

        response = client.get(
            f"/goals/goal/{goal.pk}"
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data == GoalSerializer(goal).data, "Incorrect data"
