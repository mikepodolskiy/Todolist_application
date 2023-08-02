from django.db import models

from django.db import models
from django.utils import timezone

from core.models import User


class DateTimeModelMixin(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", blank=True, null=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Board(DateTimeModelMixin):
    title = models.CharField(max_length=255, verbose_name="Название")
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    def __str__(self):
        return self.title


class GoalCategory(DateTimeModelMixin):
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    board = models.ForeignKey(
        "Board",
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="categories",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Goal(DateTimeModelMixin):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(verbose_name="Название", max_length=150)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    category = models.ForeignKey(GoalCategory, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус",
        choices=Status.choices,
        default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет",
        choices=Priority.choices,
        default=Priority.medium
    )
    due_date = models.DateField(verbose_name='Дедлайн', null=True, blank=True)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.title


class Comment(DateTimeModelMixin):
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.CharField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class BoardParticipant(DateTimeModelMixin):
    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.reader)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="participants")
    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
