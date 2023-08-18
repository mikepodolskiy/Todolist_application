import pytest
from tests.factories import GoalCategoryFactory


class TestBoardDestroy:

    @pytest.mark.django_db
    def test_board_destroy(self, client_and_board, user_pwd_combo):
        user, _ = user_pwd_combo
        client, board = client_and_board
        categories = GoalCategoryFactory.create_batch(user=user, board=board, size=3)

        response = client.delete(f"/goals/board/{board.pk}")
        assert response.status_code == 204, f"{response.status_code} instead of 204"

        board.refresh_from_db()
        assert board.is_deleted, "Board was not marked as deleted"

        for category in categories:
            category.refresh_from_db()
            assert category.is_deleted, "Category was not marked as deleted"
