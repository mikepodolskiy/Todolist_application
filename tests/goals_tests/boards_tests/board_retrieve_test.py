import pytest
from rest_framework.status import HTTP_200_OK

from goals.serializers.board_serializers import BoardSerializer


class TestBoardRetrieve:
    @pytest.mark.django_db
    def test_board_retrieve(self, client_and_board):
        client, board = client_and_board

        response = client.get(
            f"/goals/board/{board.pk}"
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data == BoardSerializer(board).data, 'Incorrect data'
