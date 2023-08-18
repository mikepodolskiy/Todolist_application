import pytest

from goals.serializers.board_serializers import BoardSerializer


class TestBoardUpdate:
    @pytest.mark.django_db
    def test_board_update(self, client_and_board):
        client, board = client_and_board

        data = {
            "title": "updated_title",
            "participants": [],
        }
        response = client.put(
            f"/goals/board/{board.pk}",
            data=data,
            content_type="application/json"
        )

        board.refresh_from_db()
        assert response.data == BoardSerializer(board).data, "Incorrect data"
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data["title"] == data["title"], "Title was not changed"
        assert response.data["updated"] != response.data["created"], "Update time was not set"
