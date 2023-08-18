import pytest

from tests.factories import CommentFactory


class TestCommentList:
    COUNT = 12
    PAGE_SIZE = 5

    @pytest.fixture
    @pytest.mark.django_db
    def get_data(self, client_and_goal):
        client, goal = client_and_goal
        comments = CommentFactory.create_batch(size=self.COUNT, user=goal.user, goal=goal)

        return client, comments, goal

    @pytest.mark.django_db
    def test_comments_list_first_page(self, get_data, response_keys):
        client, comments, goal = get_data

        response = client.get(
            f"/goals/goal_comment/list",
            {"limit": self.PAGE_SIZE, "goal": goal.pk}
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data["previous"] is None, "Previous page link should not exist"
        assert response.data["count"] == self.COUNT, "Wrong quantity of elements"
        assert len(response.data["results"]) == self.PAGE_SIZE, "Wrong quantity of elements to show"
