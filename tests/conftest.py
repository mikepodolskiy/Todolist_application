import pytest

from goals.models import BoardParticipant
from tests.factories import UserFactory, BoardParticipantFactory, BoardFactory, GoalCategoryFactory, GoalFactory
from pytest_factoryboy import register


register(UserFactory)
register(BoardFactory)
register(GoalCategoryFactory)
register(BoardParticipantFactory)



@pytest.fixture
def password():
    return '2defb408d063ff869816'

#
@pytest.fixture
@pytest.mark.django_db
def user_pwd_combo(password):
    user = UserFactory()
    user.set_password(password)
    user.save()

    return user, password

@pytest.fixture
@pytest.mark.django_db
def client_and_user(client, user_pwd_combo):
    user, _ = user_pwd_combo
    client.force_login(user)

    return client, user


@pytest.fixture
@pytest.mark.django_db
def user_and_board(user_pwd_combo, board):
    user, _ = user_pwd_combo
    BoardParticipantFactory.create(user=user, board=board, role=BoardParticipant.Role.owner)

    return board


@pytest.fixture
@pytest.mark.django_db
def client_and_board(client_and_user, user_and_board):
    client, _ = client_and_user
    return client, user_and_board

@pytest.fixture
def response_keys():
    return {'count', 'next', 'previous', 'results'}


@pytest.fixture
@pytest.mark.django_db
def client_and_category(user_pwd_combo, client_and_board):
    user, _ = user_pwd_combo
    client, board = client_and_board
    category = GoalCategoryFactory.create(user=user, board=board)

    return client, category

@pytest.fixture
@pytest.mark.django_db
def client_and_goal(client_and_user, client_and_category):
    client, category = client_and_category
    goal = GoalFactory.create(user=category.user, category=category)

    return client, goal
