import pytest

from goals.serializers.category_serializers import GoalCategorySerializer


class TestCategoryRetrieve:
    @pytest.mark.django_db
    def test_category_retrieve(self, client_and_category):
        client, category = client_and_category

        response = client.get(
            f"/goals/goal_category/{category.pk}"
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data == GoalCategorySerializer(category).data, "Incorrect data"
