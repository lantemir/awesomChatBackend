from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

class TextModel(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор',
        to = User,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name='Текст',
        max_length=500,
    )
    created_datetime = models.DateTimeField(
        default=timezone.now,
        verbose_name="Время создания"
    )

