import datetime

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from core.models import User
from goals.models import Board, GoalCategory, BoardParticipant, Goal, Comment


class UniqueFaker(Faker):
    def evaluate(self, instance, step, extra):
        locale = extra.pop('locale')
        subfaker = self._get_faker(locale)
        unique_proxy = subfaker.unique
        return unique_proxy.format(self.provider, **extra)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name: Faker = Faker("first_name")
    last_name: Faker = Faker("last_name")
    email: UniqueFaker = UniqueFaker("email")
    username: UniqueFaker = UniqueFaker("name")


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    title: Faker = Faker('name')


class GoalCategoryFactory(DjangoModelFactory):
    class Meta:
        model = GoalCategory

    user: SubFactory = SubFactory(UserFactory)
    title: Faker = Faker('name')
    board: SubFactory = SubFactory(BoardFactory)


class BoardParticipantFactory(DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board: SubFactory = SubFactory(BoardFactory)
    user: SubFactory = SubFactory(UserFactory)
    role = BoardParticipant.Role.reader


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    title: UniqueFaker = UniqueFaker('name')
    description: UniqueFaker = UniqueFaker('sentence')
    category: SubFactory = SubFactory(GoalCategoryFactory)
    user: SubFactory = SubFactory(UserFactory)
    priority = Goal.Priority.low
    status = Goal.Status.to_do
    due_date = datetime.date.today()


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    user: SubFactory = SubFactory(UserFactory)
    goal: SubFactory = SubFactory(GoalFactory)
    text: Faker = Faker('sentence')
