import pytest
from goals.models import GoalCategory

class TestCategoryCreate:
    @pytest.mark.django_db
    def test_category_create(self, client_and_user, user_and_board):
        client, user = client_and_user

        data = {
            "title": "new_title",
            "board": user_and_board.id,
        }
        response = client.post(
            "/goals/goal_category/create",
            data=data,
            content_type="application/json"
        )
        assert response.status_code == 201, f"{response.status_code} instead of 201"

        created_category = GoalCategory.objects.last()
        assert created_category.title == data["title"], "Incorrect title"
        assert created_category.user == user, "Incorrect user"
        assert created_category.board == user_and_board, "Incorrect board"
        assert created_category.created is not None, "Creation date absent"
        assert created_category.updated is not None, "Update date absent"
