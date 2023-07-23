from django.db import models

from django.db import models
from django.utils import timezone

from core.models import User

class GoalsModelMixin(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", blank=True, null=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

class GoalCategory(GoalsModelMixin):
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Goal(GoalsModelMixin):
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


class Comment(GoalsModelMixin):
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.CharField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
