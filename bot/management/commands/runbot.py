from collections import namedtuple
from typing import Any, Type, Optional, List

from django.core.management import BaseCommand
from django.db import IntegrityError

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory, BoardParticipant
from goals.serializers.category_serializers import GoalCategorySerializer
from goals.serializers.goal_serializers import GoalSerializer


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.users = {}

    def handle(self, *args, **kwargs: Any) -> None:
        """
        launches bot and controls answering only to new message
        """
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            if not res:
                continue
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        """
        verify tg user - checks verification code, gives verification code if there was no verification before
        continues if user was verified
        """
        tg_user, _ = TgUser.objects.get_or_create(tg_chat_id=msg.chat.id, defaults={"username": msg.chat.username})
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(msg.chat.id, f"Your verification code:\n {tg_user.verification_code}")

        else:
            # self.tg_client.send_message(msg.chat.id, f"You've already verified")
            self.handle_auth_user(tg_user, msg)

    def handle_auth_user(self, tg_user: TgUser, msg: Message) -> None:
        """
        receiving text from telegram user, choosing scenario to launch, depends on message text
        """
        text = None
        chat_id = msg.chat.id
        if msg.text.startswith("/"):
            if msg.text == "/goals":
                text = self.send_goals(user_id=tg_user.user_id)

            elif msg.text == "/create":
                text, self.users = self.send_cat(user_id=tg_user.user.id, msg=msg)

            elif msg.text == "/cancel":
                try:
                    if self.users[msg.chat.id]:
                        del self.users[msg.chat.id]
                    text = 'Creation cancelled'
                except:
                    text = 'Creation cancelled'

            else:
                self.tg_client.send_message(chat_id, "Unknown command \nType /goals or /create or /cancel")

        elif chat_id in self.users:
            next_handler = self.users[chat_id].get("next_handler")
            text = next_handler(
                user_id=tg_user.user.id,
                chat_id=chat_id,
                message=msg.text,
                users=self.users
            )

        else:
            text = self.tg_client.send_message(chat_id, f"Append / please")

        if text:
            self.tg_client.send_message(chat_id=chat_id, text=text)

    def send_goals(self, user_id: Type[int]) -> Optional[Message, str]:
        """
        processing data with goals and forms message to send
        """
        goals = self._get_goals(user_id)
        if not goals.exists():
            return "Goals not found"

        data = self._get_goals_data(goals)
        message = self._make_goals_message(data)
        return message

    def send_cat(self, user_id: Optional[int, Type[int]], msg: Message) -> Optional[str, Message, dict]:
        """
        processing data with categories, forms message and users dict, set next handler
        """
        chat_id = msg.chat.id
        users = {}
        categories = self._get_cats(user_id)
        if not categories.exists():
            return "No categories was found. Please create one to create goal"
        cats_data = self._get_cats_data(categories)

        users[chat_id] = {index: item.cat_id for index, item in enumerate(cats_data, start=1)}
        users[chat_id]['next_handler'] = self.choose_cat

        message = self._make_cats_message(cats_data)

        return message, users

    def choose_cat(self, **kwargs) -> str:
        """
        processing users dict data, determining next handler, save category from message to users dict

        """
        chat_id = kwargs.get("chat_id")
        message = kwargs.get("message")
        users = kwargs.get("users")

        if message.isdigit():
            val = int(message)
            category_id = users.get(chat_id, {}).get(val)
            if category_id:
                users[chat_id]["next_handler"] = self.create_goal
                users[chat_id]['category_id'] = category_id
                return f"Category {val} was chosen. Set the goal name"
            else:
                return f"Invalid category {category_id}"
        else:
            return "Category index not valid"

    def create_goal(self, **kwargs) -> str:
        """
        collect data from message and users, create and save new goal with all data that was collected
        """
        user_id = kwargs.get('user_id')
        chat_id = kwargs.get('chat_id')
        message = kwargs.get('message')
        users = kwargs.get('users')
        try:
            category_id = users.get(chat_id, {}).get('category_id')
            Goal.objects.create(title=message, user_id=user_id, category_id=category_id)
            users.pop(chat_id, None)
            return f"Goal {message} added"
        except IntegrityError:
            return "Goal was not created"
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_goals(self, user_id: Type[int]) -> List:
        """
        collect data with user's goals from db
        """
        goals = (
            Goal.objects.select_related('user')
            .filter(category__board__participants__user_id=user_id, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
            .all()
        )
        return goals

    def _get_cats(self, user_id: Type[int]) -> List:
        """
        collect data with user's categories from db
        """
        categories = (
            GoalCategory.objects.select_related('user')
            .filter(
                board__participants__user_id=user_id,
                board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer])
            .exclude(is_deleted=True)
            .all()
        )
        return categories

    def _get_goals_data(self, data: List) -> List:
        """
        packs goals data to required form

        """
        serializer = GoalSerializer(data, many=True)
        goals_data = [{
            "title": goal_data["title"],
            "description": goal_data["description"],
            "category": goal_data["category"],
            "due_date": goal_data["due_date"],
            "status": goal_data["status"],

        } for goal_data in serializer.data]

        return goals_data

    def _get_cats_data(self, data):
        """
        packs categories data to required form
        """
        serializer = GoalCategorySerializer(data, many=True)
        cats_data = [CatData(cat_id=cat_data["id"], title=cat_data["title"]) for cat_data in serializer.data]

        return cats_data

    def _make_goals_message(self, data: List) -> str:
        """
        transform goals data to string to send
        """
        raw_message = [f"{item['title']}|"
                       f"description: {item['description']} |"
                       f"category: {item['category']} |"
                       f"due_date: {item['due_date']} |"
                       f"status: {item['status']} |\n"
                       for item in data]
        message = '\n'.join(raw_message)
        return message

    def _make_cats_message(self, data) -> str:
        """
        transform categories data to string to send
        """

        raw_message = [f'{index}) {item.title}' for index, item in enumerate(data, start=1)]
        message = '\n'.join(raw_message)
        return message


CatData = namedtuple('CatData', ['cat_id', 'title'])
