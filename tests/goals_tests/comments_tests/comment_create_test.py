import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from goals.models import Comment
from tests.factories import GoalFactory


class TestCommentCreate:
    @pytest.mark.django_db
    def test_comment_create(self, client_and_user, client_and_goal):
        client, goal = client_and_goal
        data = {
            "text": "new_comment",
            "goal": goal.pk,
        }
        response = client.post(
            "/goals/goal_comment/create",
            data=data,
            content_type="application/json"
        )
        assert response.status_code == 201, f"{response.status_code} instead of 201"
        created_comment = Comment.objects.last()

        assert created_comment.text == data["text"], "Incorrect title"
        assert created_comment.goal == goal, "Incorrect comment's goal"
        assert created_comment.user == goal.user, "Incorrect comment's author"
        assert created_comment.created is not None, "Creation date is absent"
        assert created_comment.updated is not None, "Update date is absent"
