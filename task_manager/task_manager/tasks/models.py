from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class FavoriteTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f'{self.user.username} - {self.task.title}'