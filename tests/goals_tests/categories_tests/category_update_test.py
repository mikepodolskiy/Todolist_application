import pytest

from goals.serializers.category_serializers import GoalCategorySerializer


class TestCategoryUpdate:
    @pytest.mark.django_db
    def test_category_update(self, client_and_category):
        client, category = client_and_category

        data = {
            "title": "new_title"
        }
        response = client.put(
            f"/goals/goal_category/{category.pk}",
            data=data,
            content_type="application/json"
        )
        category.refresh_from_db()
        assert response.data == GoalCategorySerializer(category).data, "Incorrect data"
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data["title"] == data["title"], "Title was not changed"
        assert response.data["updated"] != response.data["created"], "Update time was not set"
