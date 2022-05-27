from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    StatusType = models.TextChoices('StatusType', 'review blocked correct')
    text = models.CharField(max_length=1024, default='sample text', blank=True, verbose_name='Текст сообщения')
    status = models.CharField(max_length=10, choices=StatusType.choices, default=StatusType.review, blank=True, verbose_name='Статус сообщения')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')


    class Meta:
        ordering = ['status']
    
    def __str__(self):
        return self.text


# Create your models here.
