import pytest

from goals.models import Board, BoardParticipant
from goals.serializers.board_serializers import BoardCreateSerializer


class TestBoardCreate:
    @pytest.mark.django_db
    def test_board_create(self, client_and_user):
        client, user = client_and_user

        data = {
            "title": "New_board_title",
        }
        response = client.post(
            "/goals/board/create",
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 201, f"{response.status_code} instead 201"

        board = Board.objects.last()
        assert response.data == BoardCreateSerializer(board).data, "Incorrect data"

        board_owner = BoardParticipant.objects.last()
        assert board_owner.user == user, "Incorrect user"
        assert board_owner.board == board, "Incorrect board"
        assert board_owner.role == BoardParticipant.Role.owner, "Incorrect user's role"
