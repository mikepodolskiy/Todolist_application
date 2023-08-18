import pytest
from tests.factories import GoalFactory


class TestGoalList:
    COUNT = 3
    LIMIT = 10

    @pytest.fixture
    def get_data(self, client_and_category):
        client, category = client_and_category
        goals = GoalFactory.create_batch(category=category, user=category.user, size=self.COUNT)
        return client, goals

    @pytest.mark.django_db
    def test_goal_list(self, get_data, response_keys):
        client, goals = get_data
        response = client.get(
            f"/goals/goal/list",
            {"limit": self.LIMIT}
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data["count"] == self.COUNT, "Wrong quantity of elements"
        assert len(response.data["results"]) == self.COUNT, "Wrong quantity of elements to show"

    @pytest.mark.django_db
    def test_goal_list_unauthorized(self, client):
        response = client.get(
            f'/goals/goal/list',
            {"limit": self.LIMIT}
        )
        assert response.status_code == 403, f"{response.status_code} вместо 403"
