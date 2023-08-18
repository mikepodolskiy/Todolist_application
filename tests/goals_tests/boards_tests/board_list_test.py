import pytest
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from goals.serializers.board_serializers import BoardListSerializer
from tests.factories import BoardFactory, BoardParticipantFactory
from goals.models import BoardParticipant


class TestBoardList:
    COUNT = 5
    PAGE_SIZE = 2

    @pytest.fixture
    @pytest.mark.django_db
    def get_boards(self, client_and_user):
        client, user = client_and_user
        boards = BoardFactory.create_batch(size=self.COUNT)
        boards.sort(key=lambda board: board.title)
        boards_owner = [BoardParticipantFactory.create(board=board, user=user, role=BoardParticipant.Role.owner)
                        for board in boards]

        return client, boards

    @pytest.mark.django_db
    def test_board_list_middle_page(self, get_boards, response_keys):
        client, boards = get_boards

        response = client.get(
            f"/goals/board/list",
            {"limit": self.PAGE_SIZE, "offset": self.PAGE_SIZE}
        )
        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data["next"] is not None, "No next page link"
        assert response.data["previous"] is not None, "No previous page link"
        assert response.data["count"] == self.COUNT, "Wrong quantity of elements"
        assert len(response.data["results"]) == self.PAGE_SIZE, "Wrong quantity of elements to show"

    @pytest.mark.django_db
    def test_board_list_last_page(self, get_boards, response_keys):
        client, boards = get_boards
        response = client.get(
            f"/goals/board/list",
            {
                "limit": self.PAGE_SIZE,
                "offset": self.PAGE_SIZE * (self.COUNT // self.PAGE_SIZE)
            }
        )

        assert response.status_code == 200, f"{response.status_code} instead of 200"
        assert response.data["next"] is None, "Next page link should not exist"
        assert response.data["previous"] is not None, "No previous page link"
        assert response.data["count"] == self.COUNT, "Wrong quantity of elements"
        assert len(response.data["results"]) == self.COUNT % self.PAGE_SIZE, "Wrong quantity of elements to show"

    @pytest.mark.django_db
    def test_board_list_unauthorized(self, client):
        response = client.get(
            f"/goals/board/list",
            {"limit": self.PAGE_SIZE, "offset": self.PAGE_SIZE}
        )
        assert response.status_code == 403, f"{response.status_code} вместо 403"