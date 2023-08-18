import pytest
from tests.factories import GoalCategoryFactory, GoalFactory


class TestCategoryDestroy:

    @pytest.mark.django_db
    def test_category_destroy(self, client_and_user, user_and_board):
        client, user = client_and_user
        category = GoalCategoryFactory.create(user=user, board=user_and_board)
        GoalFactory.create_batch(size=2, category=category)

        response = client.delete(f"/goals/goal_category/{category.pk}")

        assert response.status_code == 204, f"{response.status_code} instead of 204"

        category.refresh_from_db()
        assert category.is_deleted, "Category was not marked as deleted"
