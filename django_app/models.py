from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver 
from django.db.models.signals import post_save

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

# def upload_thumbnail(instance, filename):
#     path = f'thubnails/{instance.username}'
#     extension= filename.split('.')[-1]
#     if extension:
#         path = path + '.' + extension
#     return path

# class User(AbstractUser):
#     thumbnail = models.ImageField(
#         upload_to=upload_thumbnail,
#         null=True,
#         blank=True
#     )

def upload_thumbnail(instance, filename):
    user = instance.user
    path = f'thubnails/{user.username}'
    extension= filename.split('.')[-1]
    if extension:
        path = path + '.' + extension
    return path


class Profile(models.Model):
    user = models.OneToOneField(
        primary_key=True,
        editable=True,
        blank=True,
        null=False,
        default=None,
        verbose_name='Аккаунт',

        to=User,
        on_delete=models.CASCADE,
    )

    avatar = models.ImageField(
        null=True,       
        blank=True,       
        upload_to=upload_thumbnail,
        default='avatars/ava.jpg'
    )    

    delivary_adres = models.CharField(
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
       
        
        verbose_name="адрес доставки",
        help_text='<small class="text-muted">это адрес доставки</small><hr><br>',
        max_length=500,
    )

    is_confirmed_email = models.BooleanField(
        default=False,

        verbose_name="имэйл подтверждён?",
        help_text='<small class="text-muted">имэйл подтверждён</small><hr><br>',
    )
    class Meta:
        app_label = 'auth'
        ordering =('user',)
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'профиль: {self.user.username}'
    


#сигнал при создании юзера автоматом создаст таблицу profile 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # тут происходит первое создание модели
        Profile.objects.get_or_create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
